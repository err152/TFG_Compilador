from Token import Token,TokenType

class Entorno:
   
   closure_function = None

   def __init__(self):
      self.values = {}
      self.stack = []
      #self.stack.append(value.values)
      #self.values = dict()
      
   
   def define(self, name:str, value:any): ##
      self.values[name] = value
      
   def ancestor(self,distance:int): ##
      ento = self
      i = 0
      while i < distance:
         ento = ento.enclose # stack? enclose?
         i = i + 1
      
   def getAt(self, distance:int, name:str): ##
      return self.ancestor(distance).values[name]
   
   def assignAt(self, distance:int, name:Token, value:any): ##
      self.ancestor(distance).values.append(name.valor,value)

   def get(self, name:Token) -> any:
      if name.valor in self.values:
         return self.values.get(name.valor)
      
      for i in reversed(self.stack):
         if name.valor in i:
            return i.get(name.valor)
      return self.closure_function.get(name)
      raise RuntimeError(name,"Undefined variable '"+name.valor+"'.")

   def assign(self, name:Token,value:any):
      if name.valor in self.values:
         self.values[name.valor] = value 
         return

      for i in reversed(self.stack):
         if name.valor in i:
            i[name.valor] = value
            break
      else:
         if self.closure_function is not None:
            self.closure_function.assign(name, value)
            return
         raise RuntimeError(name,"Undefined variable '"+name.valor+"'.")
   
   def enter_scope(self):
      self.stack.append(self.values)
      self.values = dict()
      
   def exit_scope(self):
      self.values = self.stack.pop()     
 
