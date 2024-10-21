import os
import cv2
import re
import fitz
import string
import psycopg2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
#from transformers import VisionEncoderDecoderModel, ViTImageProcessor, RobertaTokenizer
from typing import List, Tuple, Optional

import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

web_s = r"/mnt/web_s"
path = os.path.join(web_s, "Mateusz/Python/pass.txt")
 
with open(path, 'r') as file:
    cred = file.read().strip()

conn = psycopg2.connect(
    dbname=name,
    user=user,
    password=cred,
    host=host,
    port=port
)

global result_ref
result_ref = set()
cur = conn.cursor()
ref ='''
SELECT client_id FROM clients
'''
cur.execute(ref)
conn.commit()
query = cur.fetchall()
result_ref = set(row[0] for row in query)

def load_model(model_path: str) -> YOLO:
    return YOLO(model_path)

def process_image(model: YOLO, image: np.ndarray, conf_threshold: float = 0.25) -> YOLO:
    return model(image, conf=conf_threshold)[0]

def create_single_box(model: YOLO, image: np.ndarray, boxes: np.ndarray, scores: np.ndarray, max_expansion: int = 200) -> Tuple[Optional[List[float]], float]:
    if len(boxes) == 0:
        return None, 0

    x1, y1 = np.min(boxes[:, [0, 1]], axis=0)
    x2, y2 = np.max(boxes[:, [2, 3]], axis=0)

    height, width = image.shape[:2]
   
    left_expansion = expand_direction(model, image, x1, y1, y2, -1, width, max_expansion)
    right_expansion = expand_direction(model, image, x2, y1, y2, 1, width, max_expansion)

    x1 = max(0, x1 - left_expansion)
    x2 = min(width, x2 + right_expansion)

    y1, y2 = adjust_vertical_bounds(image, x1, x2, y1, y2)

    return [x1, y1, x2, y2], float(np.max(scores))

def expand_direction(model: YOLO, image: np.ndarray, x: float, y1: float, y2: float, direction: int, limit: int, max_expansion: int) -> int:
    y1, y2 = int(y1), int(y2)
    x = int(x)
    expansion = 0
    step = 10

    while expansion < max_expansion:
        next_x = x + direction * (expansion + step)
        if next_x < 0 or next_x >= limit:
            break
       
        sub_image = image[y1:y2, x:next_x] if direction > 0 else image[y1:y2, next_x:x]
       
        results = process_image(model, sub_image)
       
        if len(results.boxes) > 0:
            expansion += step
        else:
            break
    return expansion

def adjust_vertical_bounds(image: np.ndarray, x1: float, x2: float, y1: float, y2: float) -> Tuple[float, float]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    region = gray[int(y1):int(y2), int(x1):int(x2)]
    rows = np.mean(region, axis=1)
    non_empty_rows = np.where(rows < 250)[0]
    if len(non_empty_rows) > 0:
        y1 = y1 + non_empty_rows[0] - 15
        y2 = y1 + non_empty_rows[-1] + 20
    return max(0, y1), min(gray.shape[0], y2)

def scale_coordinates(box: List[float], scale: float, cropped_height: int, original_height: int) -> List[float]:
    x1, y1, x2, y2 = box
    scaled_x1 = x1 / scale
    scaled_x2 = x2 / scale
    scaled_y1 = y1 / scale
    scaled_y2 = y2 / scale

    full_scaled_y1 = scaled_y1
    full_scaled_y2 = scaled_y2

    return [scaled_x1, full_scaled_y1, scaled_x2, full_scaled_y2]

def extract_images_from_pdf(pdf_path: str, scale: float = 0.75) -> List[Tuple[np.ndarray, np.ndarray, float]]:
    doc = fitz.open(pdf_path)
    images = []
    for page in doc[:3]:
        pix_full = page.get_pixmap()
        img_full = np.frombuffer(pix_full.samples, dtype=np.uint8).reshape(pix_full.height, pix_full.width, pix_full.n)
        img_full = cv2.cvtColor(img_full, cv2.COLOR_RGB2BGR)
       
        pix_scaled = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        img_scaled = np.frombuffer(pix_scaled.samples, dtype=np.uint8).reshape(pix_scaled.height, pix_scaled.width, pix_scaled.n)
        img_scaled = cv2.cvtColor(img_scaled, cv2.COLOR_RGB2BGR)
       
        height, width = img_scaled.shape[:2]
        top_third_scaled = img_scaled[:height // 3, :, :] # Process top 1/3 of the page
       
        images.append((top_third_scaled, img_full, scale))
    return images

def find_ref(model: YOLO, scaled_image: np.ndarray, full_image: np.ndarray, scale: float) -> Tuple[Optional[str], Optional[List[float]]]:
    detection_results = process_image(model, scaled_image)
   
    boxes = detection_results.boxes.xyxy.cpu().numpy()
    scores = detection_results.boxes.conf.cpu().numpy()
   
    expanded_box, max_score = create_single_box(model, scaled_image, boxes, scores)
   
    if expanded_box is not None:
        visualize_img = scaled_image.copy()
        x1, y1, x2, y2 = map(int, expanded_box)

        full_x1, full_y1, full_x2, full_y2 = [int(coord / scale) for coord in [x1, y1, x2, y2]]
        roi = full_image[full_y1:full_y2, full_x1:full_x2]
        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        name = perform_tocr(Image.fromarray(roi_rgb)).replace(' ', '')
       
        if name.isdigit() and name in result_ref:
            return name, [full_x1, full_y1, full_x2, full_y2]
   
    return None, None

def ref_bbox(pdf_path: str, model: YOLO) -> Tuple[Optional[str], Optional[List[float]]]:
    images = extract_images_from_pdf(pdf_path)
   
    for scaled_img, full_img, scale in images:
        name, box = find_ref(model, scaled_img, full_img, scale)
        if name:
            return name, box
   
    return None, None

def perform_tocr(roi_image):
    pixel_values = processor(images=roi_image, return_tensors="pt").pixel_values
    output = model.generate(pixel_values)
    name = processor.batch_decode(output, skip_special_tokens=True)[0]
    return name

def process_pdf(pdf_path: str, model: YOLO):
    name, box = ref_bbox(pdf_path, model)
    doc = fitz.open(pdf_path)
    return name, box

def main():
    base_folder = r"/mnt/c/Users/Mateusz/transform/r"
    error_folder = os.path.join(base_folder, "review")
    model_path = r"C:\Users\Mateusz\model\yolov8s_handwritten_digits_v002.pt"
   
    model = load_model(model_path)
    pdf_files = [f for f in os.listdir(base_folder) if f.lower().endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(base_folder, pdf_file)
        name, title, box = process_pdf(pdf_path, model)
       
        if name:
            new_filename = f"{name}.pdf"
        while os.path.exists(os.path.join(base_folder, new_filename)):
            i = 1
            new_filename = f"{name}_{i}.pdf"
            i += 1
           
            new_path = os.path.join(base_folder, new_filename)
            os.rename(pdf_path, new_path)
        else:
            os.makedirs(error_folder, exist_ok=True)
            os.rename(pdf_path, os.path.join(error_folder, pdf_file))

if __name__ == "__main__":
    main()