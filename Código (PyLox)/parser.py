# sum: NUMBER | NUMBER ‘+’ sum

def sum(lista_tokens):
    valor = 0
    t = siguiente_token(lista_tokens)
    if t == 'NUMBER':
        valor = valor + t
        descarta(lista_tokens)
        if siguiente_token(lista_tokens) == '+':
            descarta(lista_tokens)
            return valor + sum(lista_tokens)
    else:
        raise Exception("No es un numero")

# res: NUMBER | NUMBER '-' res

def res(lista_tokens):
    valor = 0
    t = siguiente_token(lista_tokens)
    if t == 'NUMBER':
        valor = valor + t
        descarta(lista_tokens)
        if siguiente_token(lista_tokens) == '+':
            descarta(lista_tokens)
            return valor + res(lista_tokens)
    else:
        raise Exception("No es un numero")

# mul: NUMBER | NUMBER '*' mul

def mul(lista_tokens):
    valor = 0
    t = siguiente_token(lista_tokens)
    if t.type == 'NUMBER':
        valor = valor + t
        descarta(lista_tokens)
        if siguiente_token(lista_tokens) == '+':
            descarta(lista_tokens)
            return valor + res(lista_tokens)
    else:
        raise Exception("No es un numero")

def arithmetic_func(funcion):
    def func_temp(lista_tokens):
        res = 0
        for i in lista_tokens:
            res = funcion(res,i)
        return res
    return func_temp

def res(x,y):
    return x-y

def sum(x,y):
    return x+y

def mul(x,y):
    return x*y

def pot(x):
    return x*x
        
