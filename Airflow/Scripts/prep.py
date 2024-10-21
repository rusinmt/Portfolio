import os
import hashlib
import shutil
import time

read = r"/mnt/c/Users/Mateusz/transform/r/read"
done = [f for f in os.listdir(read) if f.endswith('.pdf') and f[:9].isdigit() and f.startswith('3')]
for _ in done:
    source = os.path.join(read, _)
    dest = os.path.join(r"/mnt/c/Users/Mateusz/transform/r", _)
    shutil.move(source, dest)

time.sleep(5)

def hash_file(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

def mnr(done_dir, n_dir, arch_dir):
    done_files = {}
    
    for filename in os.listdir(done_dir):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(done_dir, filename)
            done_files[hash_file(file_path)] = filename
    
    for filename in os.listdir(n_dir):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(n_dir, filename)
            file_hash = hash_file(file_path)
            
            if file_hash in done_files:
                done_filename = done_files[file_hash]
                n_filename_stripped = filename.replace("r_", "")

                for arch_filename in os.listdir(arch_dir):
                    if arch_filename == n_filename_stripped:
                        old_path = os.path.join(arch_dir, arch_filename)
                        new_path = os.path.join(arch_dir, done_filename)
                        shutil.move(old_path, new_path)
                        break
                else:
                    print(f"{n_filename_stripped} not found in {arch_dir}")

done_dir = r"/mnt/c/Users/Mateusz/transform/r/done"
n_dir = r"/mnt/c/Users/Mateusz/transform/r"
arch_dir = r"/mnt/c/Users/Mateusz/transform"

mnr(done_dir, n_dir, arch_dir)