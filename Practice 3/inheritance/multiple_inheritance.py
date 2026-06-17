# Example 1
class A:
    def f(self):
        print("A")

class B:
    def g(self):
        print("B")

class C(A, B):
    pass

c = C()
c.f(); c.g()


# Example 2
class A:
    def f(self):
        print("A")

class B(A):
    def f(self):
        print("B")

class C(B, A):
    pass

C().f()


# Example 3
class A:
    x = 10

class B:
    y = 20

class C(A, B):
    pass

c = C()
print(c.x, c.y)