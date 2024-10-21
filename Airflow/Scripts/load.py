import os
import shutil 

arch = r"/mnt/archiwum"
arch_dir = r"/mnt/c/Users/Mateusz/transform"
op = os.path.join(arch, "matched_client_id")
re = os.path.join(arch, "review")

done = [f for f in os.listdir(arch_dir) if f.endswith('.pdf') and f[:9].isdigit() and f.startswith('3')]

for _ in done:
    source = os.path.join(arch_dir, _)
    dest = os.path.join(op, _)
    if _  not in os.listdir(op):
        try:
            shutil.move(source, dest)
        except OSError as e:
            if e.errno == 18:
                shutil.copy2(source, dest)
        
read = [f for f in os.listdir(arch_dir) if f.endswith('.pdf') and f not in done]

for _ in read:
    source = os.path.join(arch_dir, _)
    dest = os.path.join(re, _)
    try:
        shutil.move(source, dest)
    except OSError as e:
        if e.errno == 18:
            shutil.copy2(source, dest)

shutil.rmtree(arch_dir)