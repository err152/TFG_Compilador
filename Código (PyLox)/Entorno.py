from Token import Token,TokenType

class Entorno:
   values = {}

   def define(self, name:str, value:any):
      self.values[name] = value

   def get(self, name:Token) -> any:
      if name.valor in self.values:
         return self.values.get(name.valor)

      raise RuntimeError(name,"Undefined variable '"+name.valor+"'.")

   def assign(self, name:Token,value:any):
      if name.valor in self.values:
         self.values[name] = value #no estoy seguro de esto : values.put(name.lexeme, value);
         return

      raise RuntimeError(name,"Undefined variable '"+name.valor+"'.")
   
