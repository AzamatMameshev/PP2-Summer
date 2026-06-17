# Example 1
class Person:
    def __init__(self):
        print("Created")

Person()


# Example 2
class Person:
    def __init__(self, name):
        self.name = name

print(Person("Alex").name)


# Example 3
class Person:
    def __init__(self, name="Unknown"):
        self.name = name

print(Person().name)