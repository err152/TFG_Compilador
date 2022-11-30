# example.py

from debugly import debug, debugmethods

@debug
def add(x,y):
    return x + y

@debug(prefix='--- ')
def sub(x,y):
    return x - y

def mul(x,y):
    return x * y

def div(x,y):
    return x / y

@debugmethods
class Spam:
    def a(self):
        pass
    def b(self):
        pass

