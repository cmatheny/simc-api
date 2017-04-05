from utils.logger import log, warn
from tornado.websocket import WebSocketHandler

class Test:
    a = 5
    b = 2
    print("Imported it")

    @classmethod
    def callit(cls, x):
        print("Called it")
        return cls.a + x / cls.b


def tester(arg):
    aTest = type(arg.__name__, (Test, arg), {})

    class TestClass1(arg, Test):
        def iam(self):
            return self.__class__.__name__

    TestClass1.__name__ = arg.__name__
    log(arg.__name__)
    return TestClass1


def tester2(arg):

    class TestClass2(arg):
        bojangle = "s"
        decor = "t2"

        def here(self):
            return "Yup"
    TestClass2.__name__ = arg.__name__
    log(arg.__name__)
    return TestClass2

#class Tester:
#    def __init__(self, decorated):
#        log(self, decorated)
#        self(decorated)
#
#    def __call__(self, decorated):
#        log(self, decorated)
#        class TestClass(decorated, Test):
#            bojangle = "s"
#            decor = "t2"
#
#            def here(self):
#                print("Yep")
#
#        TestClass.__name__ = decorated.__name__
#        return TestClass
#
#class Tester2:
#    def __init__(self, decorated):
#        log(self, decorated)
#        self(decorated)
#
#    def __call__(self, decorated):
#        log(self, decorated)
#        class TestClass2(decorated):
#            bojangle = "s"
#            decor = "t2"
#
#            def here(self):
#                print("Yep")
#
#        TestClass2.__name__ = decorated.__name__
#        log(TestClass2)
#        return TestClass2


@tester
@tester2
class Test2:

    c = "pie"


@tester
@tester2
class Test3:

    c = "pie"


log(Test2.__dict__.keys())


test = Test2()
test2 = Test3()
log(test)

log(Test2)

log(test.__class__.__bases__)
log(Test2.a, Test2.b, Test2.c, sep="   ")
log(test.a, test.b, test.c, test.bojangle, sep="   ")
log(test2.a, test2.b, test2.c, test2.bojangle, sep="   ")
test2.here()
log(test2.iam())
warn([klass for klass in globals()])
log(globals()['Test2'].decor is "t2")
