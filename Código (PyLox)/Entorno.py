from Token import Token,TokenType
import copy

class Entorno:
   values = {}
   stack = []

   def __init__(self,value=None):
      #print("Se ha creado un Entorno")
      self.enclose = value
   
   def define(self, name:str, value:any):
      self.values[name] = value

   def get(self, name:Token) -> any:
      if name.valor in self.values:
         return self.values.get(name.valor)
      
      for i in reversed(self.stack):
         if name.valor in i:
            return i.get(name.valor)
      '''
      #print("fuera get")
      if self.enclose is not None:
         #print("Dentro get enclose = ",self.enclose)
         return self.enclose.get(name)
      '''
      raise RuntimeError(name,"Undefined variable '"+name.valor+"'.")

   def assign(self, name:Token,value:any):
      if name.valor in self.values:
         self.values[name.valor] = value #no estoy seguro de esto : values.put(name.lexeme, value);
         return

      #print("fuera assign")
      '''
      if self.enclose is not None:
         #print("Dentro assign enclose = ",self.enclose)
         self.enclose.assign(name,value)
         return
      '''
      for i in reversed(self.stack):
         if name.valor in i:
            i[name.valor] = value
            break
      else:
         raise RuntimeError(name,"Undefined variable '"+name.valor+"'.")
   
   def enter_scope(self):
      self.stack.append(self.values)
      self.values = dict()
      
   def exit_scope(self):
      self.values = self.stack.pop()
   
