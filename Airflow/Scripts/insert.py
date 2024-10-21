import os
import shutil
import datetime
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError

arch = r"/mnt/archiwum"
source_dir = r"/mnt/c/Users/Mateusz/Desktop/test"
if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        
move = [f for f in os.listdir(arch) if f.endswith('.pdf')]
midnight = datetime.date.today() - datetime.timedelta(days=0)
btf = datetime.datetime.combine(midnight, datetime.time.min)

for _ in move:
    filepath = os.path.join(arch, _)
    t = os.path.getmtime(filepath)
    mt =  datetime.datetime.fromtimestamp(t)
    if mt < btf:
        shutil.move(filepath, os.path.join(source_dir, _))

def copy_3(source_dir, dest_dir):
    for filename in os.listdir(source_dir):
        if filename.lower().endswith('.pdf'):
            source_path = os.path.join(source_dir, filename)
            dest_filename = f"r_{filename}"
            dest_path = os.path.join(dest_dir, dest_filename)
            try:
                with open(source_path, 'rb') as source_file:
                    pdf_reader = PdfReader(source_file)
                    pdf_writer = PdfWriter()

                    for page in range(min(3, len(pdf_reader.pages))):
                        pdf_writer.add_page(pdf_reader.pages[page])

                    with open(dest_path, 'wb') as dest_file:
                        pdf_writer.write(dest_file)
            except (PdfReadError, OSError, ValueError) as e:
                print(f'{e}\nnext')

dest_dir = os.path.join(source_dir, "r")
os.makedirs(dest_dir)
copy_3(source_dir, dest_dir)