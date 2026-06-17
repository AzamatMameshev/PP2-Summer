# Example 1
class A:
    def greet(self):
        print("Hello")

class B(A):
    pass

B().greet()


# Example 2
class A:
    x = 10

class B(A):
    pass

print(B().x)


# Example 3
class A:
    def f(self):
        print("A")

class B(A):
    def g(self):
        print("B")

b = B()
b.f(); b.g()