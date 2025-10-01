# baseline_scan.py
import os
import pathlib as pl
import hashlib as hl
import time
from datetime import datetime as dt

hash_file = r"C:\Users\PC\Desktop\nscs-system\Anti-virus\Collected_Hashes.txt"
infected_file = r"C:\Users\PC\Desktop\nscs-system\Anti-virus\virus_Hashes.txt"
Hashes_database = []
exist = False
readable = ""
start_path="C:\\"

def CHECK_IF_EXIST():
    global Hashes_database
    global readable
    #if TXT file not exist - make it 
    if not os.path.exists(hash_file):
        with open(hash_file, "w") as f:
            pass 
        # import the hashes from the TXT file
    with open(hash_file, "r", encoding="utf-8") as f:
        if not f.read().strip():
            start_scan()
            with open(hash_file, "r", encoding="utf-8") as f2:
                Hashes_database = [line.strip() for line in f2 if line.strip()]
        else:
            Hashes_database = [line.strip() for line in f if line.strip()]
            
    unix_time = time.time()
    readable = dt.fromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M:%S")  





def start_scan():
    for root, dirs, files in os.walk(start_path):
        for i in files:
            FILE_DATA = pl.Path(root, i)
            set_sha256_Hash(FILE_DATA, FILE_DATA.parent, FILE_DATA.name)
            
def set_sha256_Hash(file, path, name):
            global Hashes_database
            hash_sha256 = hl.sha256()
            try:
                with open(file, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
            except (PermissionError, OSError) as e:
                print(f"[!] Cannot read file: {file} -> {e}")
                return
            file_hash = hash_sha256.hexdigest()
            with open(hash_file, "a" ,encoding="utf-8") as f:
                f.write(file_hash + "," + str(path) + "," + str(name) + "," + str(readable) + "\n")    
                Hashes_database.append(file_hash)

print("Scanned files finished... comparing hashes with known viruses hashes")

####### Initial compare hashes
def scan_against_database():
    """
    Compare collected file hashes against a database of known infected hashes.
    Prints results for each hash and stops if a match is found.
    """
    # Load known infected hashes from file
    with open(infected_file, "r") as f:
        list_infected_hashes = [line.strip() for line in f if line.strip()]

    # Compare each hash
    for Hash in Hashes_database:
        print("Checking integrity of:", Hash)

        if Hash in list_infected_hashes:
            print(Hash, "is a virus!!!")
            return True   # found infection
        else:
            print("No virus found")

    return False  # no infection found
        
### for checking - make 3 programs in a random place in your computer, export the hashes of them and run a scan to see if anti virus found them
