# Example 1
class A:
    def f(self):
        print("A")

class B(A):
    def f(self):
        print("B")

B().f()


# Example 2
class A:
    def greet(self):
        print("Hello")

class B(A):
    def greet(self):
        print("Hi")

B().greet()


# Example 3
class A:
    def x(self):
        return 10

class B(A):
    def x(self):
        return 20

print(B().x())