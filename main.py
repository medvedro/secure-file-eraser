import os
import multiprocessing
import secrets
import shutil

OVERWRITE_PASSES = 35  
NOISE_SIZE = 1024  

def secure_erase_file(file_path):
    file_size = os.path.getsize(file_path)

    with open(file_path, 'rb+') as file_handle:
        for _ in range(OVERWRITE_PASSES):
            file_handle.seek(0)
            for _ in range(file_size):
                random_bytes = os.urandom(1)
                if secrets.randbelow(10) < 8:  
                    file_handle.write(random_bytes)
                else:  
                    original_byte = file_handle.read(1)
                    file_handle.write(original_byte)
                file_handle.seek(0)
                byte_pos = secrets.randbelow(file_size)
                file_handle.seek(byte_pos)
                byte = file_handle.read(1)
                modified_byte = bytes([byte[0] ^ (1 << secrets.randbelow(8))])
                file_handle.seek(byte_pos)
                file_handle.write(modified_byte)

    with open(file_path, 'ab') as file_handle:
        random_noise = os.urandom(NOISE_SIZE)
        file_handle.write(random_noise)

    os.remove(file_path)
    print("Erased file ->", file_path.lower())

def secure_erase_directory(directory):
    file_count = 0
    erased_file_count = 0

    for root, dirs, files in os.walk(directory):
        file_count += len(files)

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            secure_erase_file(file_path)
            erased_file_count += 1
            print(f"Erased: {erased_file_count}/{file_count} files", end='\r')

    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            shutil.rmtree(dir_path)
            print("Removed directory - >", dir_path.lower())

def secure_erase_drive(drive_path):
    file_count = 0
    erased_file_count = 0

    for root, dirs, files in os.walk(drive_path):
        file_count += len(files)

    for root, dirs, files in os.walk(drive_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            secure_erase_file(file_path)
            erased_file_count += 1
            print(f"Erased: {erased_file_count}/{file_count} files", end='\r')

    secure_erase_directory(drive_path)

def main():
    while True:
        erasing_path = input("[ + ] Drive or Directory Path: ")
        if os.path.exists(erasing_path):
            break
        else:
            print("Invalid path. Please enter a valid drive or directory path.")

    process_count = multiprocessing.cpu_count() 

    print("\n[ - ] Starting the erasing process...")
    pool = multiprocessing.Pool(processes=process_count)
    pool.map(secure_erase_drive, [erasing_path])
    pool.close()
    pool.join()

    print("\n[ + ] Erasing process completed.")

    # Securely delete the drive or directory itself
    if os.path.isdir(erasing_path):
        shutil.rmtree(erasing_path)
        print("Removed directory - >", erasing_path.lower())
    else:
        print("Secure erasure of drives is not supported in this script.")

if __name__ == "__main__":
    main()
