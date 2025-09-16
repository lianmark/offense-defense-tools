# baseline_scan.py
import os
import pathlib as pl
import hashlib as hl
import time
from datetime import datetime as dt

hash_file = r"C:\Users\PC\Desktop\nscs-system\Anti-virus\Collected_Hashes.txt"
Hashes_database = []

def run_baseline_scan(start_path="C:\\"):
    global Hashes_database
    #if TXT file not exist - make it 
    if not os.path.exists(hash_file):
        with open(hash_file, "w") as f:
            pass 
        
    # import the hashes from the TXT file
    with open(hash_file, "r") as f:
        Hashes_database = [line.strip() for line in f if line.strip()]
        
    #if empty 
    if not Hashes_database:
        unix_time = time.time()
        readable = dt.fromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M:%S")  
    else:
        print("skipped") 
        
    #get the hashes out of files + write it in the TXT file
    def get_sha256_Hash(file, path, name):
        hash_sha256 = hl.sha256()
        try:
            with open(file, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
        except (PermissionError, OSError) as e:
            print(f"[!] Cannot read file: {file} -> {e}")
            return
        file_hash = hash_sha256.hexdigest()
        with open(hash_file, "a") as f:
            f.write(file_hash + "," + str(path) + "," + str(name) + "," + str(readable) + "\n")    
            
        for root, dirs, files in os.walk(start_path):
            for i in files:
                FILE_DATA = pl.Path(root, i)
                get_sha256_Hash(FILE_DATA, FILE_DATA.parent, FILE_DATA.name)

run_baseline_scan()

print("Scanned files finished... comparing hashes with known viruses hashes")

####### Initial compare hashes
infected_Hashes = r"C:\Users\PC\Desktop\nscs-system\Anti-virus\virus_Hashes.txt"
with open(infected_Hashes, "r") as f: 
    list_infected_hashes = [line.strip() for line in f if line.strip()]

for Hash in Hashes_database:
    print("Checking integrity of: ", Hash)
    
    if Hash in list_infected_hashes:
        print(Hash, " is a virus!!!")
        break
    else:
        print("No virus found")
        
        
### TO-DO: make 3 programs in a random place in your computer, export the hashes of them and run a scan to see if anti virus found them
