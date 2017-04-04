
class Test:
    a=5
    b=2
    print("Ran it")
    @classmethod
    def callit(cls, x):
        return cls.a + x / cls.b
        
