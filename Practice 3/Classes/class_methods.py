# Example 1
class Person:
    def greet(self):
        print("Hello")

Person().greet()


# Example 2
class Person:
    def set_name(self, name):
        self.name = name

p = Person()
p.set_name("Bob")
print(p.name)


# Example 3
class Person:
    def add(self, a, b):
        return a + b

print(Person().add(2, 3))