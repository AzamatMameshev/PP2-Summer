import shutil
import os

os.makedirs("test_dir", exist_ok=True)

if os.path.exists("example.txt"):
    shutil.move("example.txt", "test_dir/example.txt")
    print("File moved.")

shutil.copy("test_dir/example.txt", "example_copy_again.txt")
print("File copied back.")