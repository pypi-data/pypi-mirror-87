from package1 import test1
from package1.t1 import t11
from package1.t1.t11 import t11 as t12

def test2():
    test1.test1()
    t11.t11()
    t12()
    print("test2 fun")


def cli():
    test2()
    print("test2 cli")

if __name__ == "__main__":
    test2()
    print("test2 main")