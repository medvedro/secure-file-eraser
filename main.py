import os
import hashlib

def main():
    erasing_directory = input("[ + ] Folder Path : ")
    os.chdir(erasing_directory)
    
    print("\nStarting the erasing process...")
    for filename in os.scandir(os.getcwd()):
        if filename.is_file():

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
                                
                                file_handle = open(file_path, 'r+')
                                file_handle.seek(0)
                                file_handle.write("xxxxxxxxxxxxxxxxxxxxxxxxx") 
                                file_handle.truncate()
                                file_handle.close()
                                
                                os.remove(file_path)
                                print("Erased file - >", file_path.lower(), " in this folder - > ", subfolder_path)
                                
                
                
        else:
            print("There is no file in this directory.")    

    os.removedirs(subfolder_path)
    print("\n[ + ] Erasing process completed.")
    

if __name__ == "__main__":
    main()
