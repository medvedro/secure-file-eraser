import os
import hashlib
import threading

def secure_erasing():
    
    patterns = [
            b'\x55', b'\xAA', b'\x92\x49\x24', b'\x49\x24\x92',
            b'\x24\x92\x49', b'\x00', b'\x11', b'\x22', b'\x33',
            b'\x44', b'\x55', b'\x66', b'\x77', b'\x88', b'\x99',
            b'\xAA', b'\xBB', b'\xCC', b'\xDD', b'\xEE', b'\xFF'
        ]
    
    erasing_directory = input("[ + ] Folder Path : ")
    os.chdir(erasing_directory)
    
    print("\n[ - ] Starting the erasing process...")
    for filename in os.scandir(os.getcwd()):
        if filename.is_file():

                for i in range(10):
                    file_size = os.path.getsize(filename)
                    
                    for i in range(file_size):
                        
                        file_handle = open(filename, 'r+')
                        file_handle.seek(0)
                        file_handle.write(patterns) 
                        file_handle.truncate()
                        file_handle.flush()
                        file_handle.close()
                    
                os.remove(filename)
                print("Erased file - > ", filename.name.lower(), " in this folder - > ", os.getcwd())
                
                
                for root, dirs, files in os.walk(erasing_directory):
                    for directory in dirs:
                        subfolder_path = os.path.join(root, directory)
                        
                        for file_name in os.listdir(subfolder_path):
                            file_path = os.path.join(subfolder_path, file_name)
                            if os.path.isfile(file_path):
                                
                                for i in range(10):
                                    file_size_2 = os.path.getsize(file_path)
                                    for i in range(file_size_2):
                                        
                                        file_handle = open(file_path, 'r+')
                                        file_handle.seek(0)
                                        file_handle.write(patterns) 
                                        file_handle.truncate()
                                        file_handle.flush()
                                        file_handle.close()
                                    
                            os.remove(file_path)
                            print("Erased file - >", file_path.lower(), " in this folder - > ", subfolder_path)
                                
        else:
            print("There is no file in this directory.")    


    for root, dirs, files in os.walk(erasing_directory):
                    for directory in dirs:
                        subfolder_path = os.path.join(root, directory)
                        os.removedirs(subfolder_path)
        
    print("\n[ + ] Erasing process completed.")
    

def main():
    
    thread1 = threading.Thread(target=secure_erasing)
    thread1.start()
    thread1.join()

if __name__ == "__main__":
    main()
