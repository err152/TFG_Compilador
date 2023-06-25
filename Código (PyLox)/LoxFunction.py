from typing import List
from LoxCallable import LoxCallable
import statements
from Interprete import Interprete
from Entorno import Entorno
from Return import Return
from copy import deepcopy

class LoxFunction(LoxCallable):
    
    def __init__(self, stat : statements.Function, clos : Entorno, isinit:bool):
        self.isInitializer = isinit
        self.declaration = stat
        self.closure : Entorno = deepcopy(clos)
        
    def bind(self, instance):
        ento : Entorno = Entorno()
        ento.define("this",instance)
        return LoxFunction(self.declaration,ento,self.isInitializer)
        
    def __str__(self) -> str:
        return "<fn "+self.declaration.name.valor+">"
        
    def arity(self) -> int:
        return len(self.declaration.params)
        
    def call(self, inter : Interprete, argu : List[any], entorno : Entorno):
        entorno.closure_function = (self.closure)
        entorno.enter_scope()
        for par, arg1 in zip(self.declaration.params, argu):
            entorno.define(par.valor,arg1)

        try:
            inter.executeBlock(self.declaration.body)
        except Return as returnValue:
            if self.isInitializer:
                return self.closure.getAt([0],"this")
            return returnValue.value
        finally:
            entorno.exit_scope()
            
        if self.isInitializer:
            return self.closure.getAt([0],"this")
        return None
        
    