import os
import hashlib
import threading

def secure_erasing():
    erasing_directory = input("[ + ] Folder Path : ")
    os.chdir(erasing_directory)
    
    print("\n[ - ] Starting the erasing process...")
    for filename in os.scandir(os.getcwd()):
        if filename.is_file():

                for i in range(10):
                    file_handle = open(filename, 'r+')
                    file_handle.seek(0)
                    file_handle.write("xxxxxxxxxxxxxxxxxxxxxxxxx") 
                    file_handle.truncate()
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
                                    file_handle = open(file_path, 'r+')
                                    file_handle.seek(0)
                                    file_handle.write("xxxxxxxxxxxxxxxxxxxxxxxxx") 
                                    file_handle.truncate()
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
