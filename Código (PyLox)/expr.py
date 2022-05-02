from abc import ABC, abstractmethod
from tokens import Token

class Expr(ABC):
    @abstractmethod
    def acepta(self):
        pass

class Binary(Expr):
    def __init__(self,left:Expr,operator:Token,right:Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def acepta(self):
        return

class Unary(Expr):
    def __init__(self,operator:Token,right:Expr):
        self.operator = operator
        self.right = right

class Grouping(Expr):
    def __init__(self,expr:Expr):
        self.expr = expr

class Literal(Expr):
    def __init__(self,value):
        self.value = value


        
