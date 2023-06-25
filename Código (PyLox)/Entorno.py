from Token import Token,TokenType

class Entorno:
   
   closure_function = None

   def __init__(self):
      self.values = {}
      self.stack = []


   def define(self, name:str, value:any): ##
      self.values[name] = value
      
      
   def list_dic(self,distances:[]):
      diccionarios = []
      if 0 in distances:
         diccionarios.append(self.values)
      for distance in distances:
         if len(self.stack) > 0 and len(self.stack)-1 >= distance:
            diccionarios.append(list(reversed(self.stack))[distance])
      return diccionarios
      
      
   def getAt(self, distances:set, name:str):
      diccionarios = self.list_dic(distances)
   
      for dic in diccionarios:
         if (a := dic.get(name,'%-_-%')) != '%-_-%':
            return a
           
      if self.closure_function is not None:
         a = self.closure_function.getAt(distances,name)
         return a
      raise RuntimeError(name,"Var no encontrada.")
   
   
   def assignAt(self, distances:set, name:Token, value:any):
      diccionarios = self.list_dic(distances)
      
      for dic in diccionarios:
         if dic.get(name,'%-_-%') != '%-_-%':
            dic[name.valor] = value
            return
         
      if self.closure_function is not None:
         a = self.closure_function.assignAt(distances,name,value)
         return
      raise RuntimeError(name,"No se pudo asignar. Var no encontrada.")


   def get(self, name:Token) -> any:
      if name.valor in self.values:
         return self.values.get(name.valor)
      
      for i in reversed(self.stack):
         if name.valor in i:
            return i.get(name.valor)
      if self.closure_function is not None:
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
 
