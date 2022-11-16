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

def res(lista_tokens):
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
        
