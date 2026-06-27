names = ["Alice", "Bob", "Charlie"]
scores = [88, 92, 79]

print("Using enumerate:")
for index, name in enumerate(names):
    print(index, name)

print("\nUsing zip:")
for name, score in zip(names, scores):
    print(name, score)