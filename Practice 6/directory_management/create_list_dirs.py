import os

os.makedirs("test_dir/sub_dir", exist_ok=True)
print("Directories created.")

print("\nDirectory contents:")
for item in os.listdir("."):
    print(item)