import os
import multiprocessing
import secrets
import shutil
import ctypes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

OVERWRITE_PASSES = 70
NOISE_SIZE = 1024
CLUSTER_SIZE = 4096

def generate_encryption_key():
    backend = default_backend()
    salt = os.urandom(16) 
    password = secrets.token_urlsafe(32) 

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(password.encode())

    return key


def encrypt_file(file_path, encryption_key):
    with open(file_path, 'rb') as file:
        data = file.read()

    encryption_key = generate_encryption_key()

    nonce = os.urandom(16)

    cipher = Cipher(algorithms.AES(encryption_key), mode=modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(data) + encryptor.finalize()

    file_name, file_extension = os.path.splitext(file_path)
    encrypted_file_path = file_name + '.encrypted' + file_extension

    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(nonce)
        encrypted_file.write(encrypted_data)

    return encrypted_file_path

def secure_erase_file(file_path):
    
    file_size = os.path.getsize(file_path)
    cluster_count = (file_size + CLUSTER_SIZE - 1) // CLUSTER_SIZE

    encryption_key = generate_encryption_key()
    encrypted_file_path = encrypt_file(file_path, encryption_key)
    
    with open(encrypted_file_path, 'rb+') as file_handle:
        for _ in range(OVERWRITE_PASSES):
            file_handle.seek(0)
            for _ in range(cluster_count):
                cluster_data = file_handle.read(CLUSTER_SIZE)
                if len(cluster_data) < CLUSTER_SIZE:
                    cluster_data += b'\x00' * (CLUSTER_SIZE - len(cluster_data))

                random_bytes = os.urandom(CLUSTER_SIZE)
                if secrets.randbelow(10) < 8:
                    file_handle.write(random_bytes)
                else:
                    file_handle.write(cluster_data)

    with open(encrypted_file_path, 'ab') as file_handle:
        random_noise = os.urandom(NOISE_SIZE)
        file_handle.write(random_noise)

    os.remove(encrypted_file_path)
    print("Erased file ->", encrypted_file_path.lower())
    
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

    if os.path.isdir(erasing_path):
        shutil.rmtree(erasing_path)
        print("Removed directory - >", erasing_path.lower())
    else:
        print("Secure erasure of drives is not supported in this script.")

if __name__ == "__main__":
    main()
