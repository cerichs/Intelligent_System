
import os

folder_path = r"C:\Users\Cornelius\Downloads\intelligentesystemer"  # Replace with the actual folder path

files = os.listdir(folder_path)

for i, file_name in enumerate(files):
    # Split the file name and extension
    file_name_parts = os.path.splitext(file_name)
    file_extension = "x.jpg"
    
    new_file_name = str(i + 1) + file_extension
    
    old_file_path = os.path.join(folder_path, file_name)
    new_file_path = os.path.join(folder_path, new_file_name)
    
    # Rename the file
    os.rename(old_file_path, new_file_path)
