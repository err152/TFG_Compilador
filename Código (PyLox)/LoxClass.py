from typing import List;
from LoxCallable import LoxCallable
from Interprete import Interprete
from Entorno import Entorno

class LoxClass(LoxCallable):
   
   def __init__(self,name:str, methods:{}):
      self.name = name
      self.methods = methods
      
   def findMethod(self, name:str) :
      if name in self.methods:
         return self.methods.get(name)
      
      return None
      
   def __repr__(self):
      return self.name
   
   def call(self, inter:Interprete, argus:[any], ento:Entorno):
      from LoxInstance import LoxInstance
      from LoxFunction import LoxFunction
      instance : LoxInstance = LoxInstance(self)
      initializer : LoxFunction = self.findMethod("init")
      if initializer is not None:
         initializer.bind(instance).call(inter,argus,ento)
      return instance
   
   def arity(self) -> int:
      initializer = self.findMethod("init")
      if initializer is None:
         return 0
      return initializer.arity()
