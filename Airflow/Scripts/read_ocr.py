import os
import shutil
import re
import string
import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text_pages = []
        for page in reader.pages:
            text_pages.append(page.extract_text())
        return text_pages

def format(title):
    invalid_chars = r'[<>:"/\\|?#*]'
    title = re.sub(invalid_chars, '_', title)
    title = re.sub(r'\d+', '', title)
    title = re.sub(r'\s*-?\d{1,2}[-./]\d{1,2}[-./]\d{2,4}\b', '', title)
    title = ' '.join(title.split())
    title = string.capwords(title)
    return title if title else ""

def custom_title(title):
    words = title.split()
    capitalized_words = []
    for word in words:
        if len(word) == 1:
            capitalized_words.append(word.lower())
        else:
            capitalized_words.append(word.capitalize())
    return ' '.join(capitalized_words)

def extract_text_from_pdf(pdf_path):
    text_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_pages.append(page.extract_text())
    return text_pages

def process_pdfs(source_folder, done_folder, read_folder):
    for filename in tqdm(os.listdir(source_folder)):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(source_folder, filename)
            try:
                text_pages = extract_text_from_pdf(pdf_path)
            except PDFSyntaxError as e:
                shutil.copy2(pdf_path, os.path.join(read_folder, filename))
            number_match = None
            title_match = None
            match_page = -1
            
            for page_num, page_text in enumerate(text_pages[:3]):
                number_match = re.search(r'\b30\d{7}\b', page_text)
                if number_match:
                    match_page = page_num
                    break
            
            if match_page != -1:
                title_pattern = r'^\b(?:ZAWIADOMIENIE|ZARZĄDZENIE|NAKAZ|WNIOSEK|APELACJA|WEZWANIE|INFORMACJA|POSTANOWIENIE|POZEW|REPLIKA|WYSŁUCHANIE|PROTOKÓŁ|KONTYNUACJA)\b.*$'
                title_match = re.search(title_pattern, text_pages[match_page], re.MULTILINE | re.IGNORECASE)
                if title_match:
                    title = title_match.group()
                    exclude = ["SYG", "SYGN", "DNI", "UL.", "TEL"]
                    for sign in exclude:
                        if title.upper().strip().endswith(sign):
                            title = title[:-(len(sign))].strip()
                    title_match = re.match(re.escape(title), title)
        
            exclude = ["SYG", "SYGN", "DNI", "UL.", "TEL"]
            
            if number_match and title_match:
                number = number_match.group()
                title = format(title_match.group())
                if title_match and match_page == 0:
                    new_filename = f"{number}_{title}.pdf"
                else:
                    i = 1
                    new_filename = f"{number}.pdf"
                    while os.path.exists(os.path.join(done_folder, new_filename)):
                        new_filename = f"{number}_{i}.pdf"
                        i += 1
                        
                shutil.copy2(pdf_path, os.path.join(done_folder, new_filename))
            elif number_match:
                number = number_match.group()
                new_filename = f"{number}.pdf"
                shutil.copy2(pdf_path, os.path.join(done_folder, new_filename))
            elif title_match:
                title = format(title_match.group())
                new_filename = f"b r a k_{title}.pdf"
                shutil.copy2(pdf_path, os.path.join(read_folder, filename))
            else:
                shutil.copy2(pdf_path, os.path.join(read_folder, filename))
               
source_folder = r"/mnt/c/Users/Mateusz/transform/r"
done_folder = os.path.join(source_folder, "done")
read_folder = os.path.join(source_folder, "read")

os.makedirs(done_folder, exist_ok=True)
os.makedirs(read_folder, exist_ok=True)

process_pdfs(source_folder, done_folder, read_folder)