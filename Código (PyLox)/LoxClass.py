from typing import List;
from LoxCallable import LoxCallable
from Interprete import Interprete

class LoxClass(LoxCallable):
   
   def __init__(self,name:str):
      self.name = name
      
   def __repr__(self):
      return self.name
   
   def call(self, inter:Interprete, argus:[any]):
      from LoxInstance import LoxInstance
      instance : LoxInstance = LoxInstance(self)
      return instance
   
   def arity(self) -> int:
      return 0
