from dataclasses import dataclass

def suma(lista_enteros):
    temp = 0
    for i in lista_enteros:
        temp = temp + i
    return temp


def resta(lista_enteros):
    temp = 0
    for i in lista_enteros:
        temp = temp - i
    return temp


def template(funcion):
    def func_temp(lista_enteros):
        temp = 0
        for i in lista_enteros:
            temp = funcion(temp, i)
        return temp
    return func_temp



resta_nueva = template(lambda x,y: x-y)

def f(x,y):
    return x + y


f = template(f)

@template
def f(x,y):
    return x + y


def debug(func):
    def temp(*args):
        print(*args, func.__name__)
        a =  func(*args)
        print(f'el resultado es:{a}')
        return a
    return temp

@debug
def f(x,y,z):
    return x * y - z

@debug
def g(x,y,z):
    return x - y - z

f(3, 2, 1)


class M0:

    def __init__(self, s, r):
        self.s = s
        self.r = r

@dataclass
class M1:
    s: int
    r: int

a = 1

d = {
    1: lambda a: a*2,
    2: lambda a: a*a,
    3: lambda a: 5**a
}

if a == 1:
    print(a*2)
elif a == 2:
    print(a*a)
elif a == 3:
    print( 5**a)

print(d[a](a))
