from package1 import test1
from package1 import test2
from package2 import test3

def test4():
    test1.test1()
    test2.test2()
    test3.test3()
    print("test4 fun")


def main1():
    test4()
    print("test4 main1 func")

if __name__ == "__main__":
    test4()
    print("test4 main")