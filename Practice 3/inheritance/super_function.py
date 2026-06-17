# Example 1
class A:
    def greet(self):
        print("Hello")

class B(A):
    def greet(self):
        super().greet()
        print("World")

B().greet()


# Example 2
class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        super().__init__()
        print("B")

B()


# Example 3
class A:
    def f(self):
        print("A")

class B(A):
    def f(self):
        super().f()
        print("B")

B().f()