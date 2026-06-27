import shutil
import os

shutil.copy("example.txt", "example_copy.txt")
print("File copied.")

file_to_delete = "example_copy.txt"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print("File deleted.")
else:
    print("File does not exist.")