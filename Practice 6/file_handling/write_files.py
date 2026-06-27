with open("example.txt", "w") as file:
    file.write("First line\n")
    file.write("Second line\n")

with open("example.txt", "a") as file:
    file.write("Appended line\n")

print("File written and appended successfully.")