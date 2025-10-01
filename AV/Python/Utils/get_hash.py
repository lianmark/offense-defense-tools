import hashlib as hl
#which file to get the hash of
hash_file = r"C:\Users\..."
# where to print the hash of the file
export_single_hash = r"C:\Users\..."

hash_sha256 = hl.sha256()
try:
    with open(hash_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
except (PermissionError, OSError) as e:
    print("error")

file_hash = hash_sha256.hexdigest()
with open(export_single_hash, "a" ,encoding="utf-8") as f:
    f.write(file_hash)    
