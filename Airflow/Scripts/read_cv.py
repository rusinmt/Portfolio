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
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, RobertaTokenizer
from typing import List, Tuple, Optional

import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

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
SELECT viitenumber FROM lepingu_lisad
'''
cur.execute(ref)
conn.commit()
query = cur.fetchall()
result_ref = set(row[0] for row in query)

def load_model(model_path: str) -> YOLO:
    return YOLO(model_path)

def process_image(model: YOLO, image: np.ndarray, conf_threshold: float = 0.25) -> List:
    return model(image, conf=conf_threshold)

def create_single_box(model: YOLO, image: np.ndarray, boxes: np.ndarray, scores: np.ndarray, max_expansion: int = 200) -> Tuple[Optional[List[float]], float]:
    if len(boxes) == 0:
        return None, 0

    x1, y1 = np.min(boxes[:, [0, 1]], axis=0)
    x2, y2 = np.max(boxes[:, [2, 3]], axis=0)
    
    height, width = image.shape[:2]
    
    left_expansion = expand_direction(model, image, x1, y1, y2, -1, width, max_expansion)
    right_expansion = expand_direction(model, image, x2, y1, y2, 1, width, max_expansion)
    
    # Apply expansions with bounds checking
    x1 = max(0, x1 - left_expansion)
    x2 = min(width, x2 + right_expansion)
    
    # Adjust vertical bounds to remove empty space
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
            
        if direction > 0:
            sub_image = image[y1:y2, x:next_x]
        else:
            sub_image = image[y1:y2, next_x:x]
            
        results = process_image(model, sub_image)
        if len(results[0].boxes) > 0:
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
        y1 = y1 + non_empty_rows[0] - 5  # Add small padding
        y2 = y1 + non_empty_rows[-1] + 10
        
    return max(0, y1), min(image.shape[0], y2)

def extract_images_from_pdf(pdf_path: str, scale: float = 0.75) -> List[Tuple[np.ndarray, np.ndarray, float]]:
    doc = fitz.open(pdf_path)
    images = []
    
    for page in doc[:3]:  # Check first 3 pages
        pix_full = page.get_pixmap()
        img_full = np.frombuffer(pix_full.samples, dtype=np.uint8).reshape(
            pix_full.height, pix_full.width, pix_full.n)
        img_full = cv2.cvtColor(img_full, cv2.COLOR_RGB2BGR)
        
        pix_scaled = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        img_scaled = np.frombuffer(pix_scaled.samples, dtype=np.uint8).reshape(
            pix_scaled.height, pix_scaled.width, pix_scaled.n)
        img_scaled = cv2.cvtColor(img_scaled, cv2.COLOR_RGB2BGR)
        
        height = img_scaled.shape[0]
        top_third = img_scaled[:height//3]
        
        images.append((top_third, img_full, scale))   
    return images

def perform_tocr(roi_image: Image) -> str:
    pixel_values = processor(images=roi_image, return_tensors="pt").pixel_values
    generated_ids = trocr_model.generate(pixel_values)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

def process_pdf(pdf_path: str, model: YOLO) -> Tuple[Optional[str], Optional[List[float]]]:
    images = extract_images_from_pdf(pdf_path)
    
    for scaled_img, full_img, scale in images:
        results = process_image(model, scaled_img)[0]
        boxes = results.boxes.xyxy.cpu().numpy()
        scores = results.boxes.conf.cpu().numpy()
        
        expanded_box, score = create_single_box(model, scaled_img, boxes, scores)
        
        if expanded_box is not None and score > 0.5:
            x1, y1, x2, y2 = [int(coord / scale) for coord in expanded_box]

            """ Preview for debuging"""
            # # Draw the bounding box on the full image
            # cv2.rectangle(full_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # # Display the image with the bounding box
            # cv2.imshow('Detected Area', full_img)
            # cv2.waitKey(0)  # Wait for a key press to close the window
            # cv2.destroyAllWindows()
            
            roi = full_img[y1:y2, x1:x2]
            roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            text = perform_tocr(Image.fromarray(roi_rgb))
            
            text = ''.join(filter(str.isdigit, text))
            if text and len(text) >= 6:  # Minimum length check
                return text, [x1, y1, x2, y2]  
    return None, None

def main():
    base_folder = r"/mnt/c/Users/Mateusz/Desktop/transform"
    model_path = r"/mnt/c/Users/Mateusz/model/yolov8s_handwritten_digits_v002.pt"
    error_folder = os.path.join(base_folder, "r")    
    os.makedirs(error_folder, exist_ok=True)
    model = load_model(model_path)
    
    for pdf_file in os.listdir(base_folder):
        if not pdf_file.lower().endswith('.pdf'):
            continue
            
        pdf_path = os.path.join(base_folder, pdf_file)
        reference, bbox = process_pdf(pdf_path, model)
        
        if reference and reference in result_ref:
            new_filename = f"{reference}.pdf"
            i = 1
            while os.path.exists(os.path.join(base_folder, new_filename)):
                new_filename = f"{reference}_{i}.pdf"
                i += 1
            
            new_path = os.path.join(base_folder, new_filename)
            os.rename(pdf_path, new_path)
        else:
            error_path = os.path.join(error_folder, pdf_file)
            os.rename(pdf_path, error_path)

if __name__ == "__main__":
    main()
