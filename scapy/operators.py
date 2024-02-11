class A:
    def __init__(self, a):
        self.a = a

    def __truediv__(self, b):
        return "This is the / operator, overloaded as binary operator."

ob1 = A(2)
ob2 = A(2)
print(ob1/ob2)