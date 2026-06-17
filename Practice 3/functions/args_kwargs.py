# Example 1
def f(*args):
    print(args)

f(1, 2, 3)


# Example 2
def f(**kwargs):
    print(kwargs)

f(name="Alex", age=25)


# Example 3
def f(*args, **kwargs):
    print(args, kwargs)

f(1, 2, x=10, y=20)