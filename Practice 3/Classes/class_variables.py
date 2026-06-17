# Example 1
class Person:
    species = "Human"

print(Person.species)


# Example 2
class Person:
    count = 0
    def __init__(self):
        Person.count += 1

Person(); Person()
print(Person.count)


# Example 3
class Person:
    x = 10

p = Person()
print(p.x)