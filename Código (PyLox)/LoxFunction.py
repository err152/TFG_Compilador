from typing import List
from LoxCallable import LoxCallable
import statements
from Interprete import Interprete
from Entorno import Entorno
from Return import Return

class LoxFunction(LoxCallable):
    
    def __init__(self, stat : statements.Function, clos : Entorno):
        self.declaration = stat
        self.closure : Entorno = clos
        
    def __str__(self) -> str:
        return "<fn "+self.declaration.name.valor+">"
        
    def arity(self) -> int:
        return len(self.declaration.params)
        
    def call(self, inter : Interprete, argu : List[any]):
        #ento : Entorno = Entorno(self.closure)
        self.closure.enter_scope()
        i = 0
        while i < len(self.declaration.params):
            self.closure.define(self.declaration.params[i].valor,argu[i])
            i = i+1
        try:
            inter.executeBlock(self.declaration.body)
        except Return as returnValue:
            return returnValue.value
        finally:
            self.closure.exit_scope()
        return None
        
    