from typing import List;
from LoxClass import LoxClass
from Token import Token,TokenType

class LoxInstance():
   
   def __init__(self,klass:LoxClass):
      self.klass = klass
      self.fields = {}
      
   def get(self, name:Token):
      if name.valor in self.fields:
         return self.fields[name.valor]
      
      raise RuntimeError(name, "Undefined property '"+name.valor+"'.")
   
   def set(self, name:Token, value:any):
      self.fields[name.valor] = value
      
   def __repr__(self) -> str:
      return self.klass.name + " instance"
   
