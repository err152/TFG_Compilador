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
      
   '''   
   def ancestor(self,distance:int): ##
      ento = self
      i = 0
      while i < distance:
         ento = ento.enclose # stack? enclose?
         i = i + 1
   ''' 
      
   def getAt(self, distances:set, name:str): ##
      for distance in distances:
         if distance == 0:               
            a = self.values.get(name,'%-_-%')
            if a != '%-_-%':
               return a
            elif len(self.stack) > 0:
               a = self.stack[-1].get(name,'%-_-%')
               if a != '%-_-%':
                  return a            
               
         elif len(self.stack) > 0:
            dist = len(self.stack) - distance - 1
            a = self.stack[dist].get(name,'%-_-%')
            if a != '%-_-%':
               return a
            
      if self.closure_function is not None:
         distances.add(0)
         a = self.closure_function.getAt(distances,name)
         return a
      raise RuntimeError(name,"Var no encontrada.")
      #return self.ancestor(distance).values[name]
   
   def assignAt(self, distances:set, name:Token, value:any): ##
      for distance in distances:
         if distance == 0:            
            a = self.values.get(name.valor,'%-_-%')
            if a != '%-_-%': 
               self.values[name.valor] = value
               return
            elif len(self.stack) > 0:
               dist = len(self.stack) - distance - 1
               a = self.stack[-1].get(name.valor,'%-_-%')
               if a != '%-_-%':
                  self.stack[dist][name.valor] = value
            
         elif len(self.stack) > 0:
            dist = len(self.stack) - distance - 1
            a = self.stack[dist].get(name.valor,'%-_-%')
            if a != '%-_-%': 
               self.stack[dist][name.valor] = value
               return
         
         if self.closure_function is not None:
            distances.add(0)
            a = self.closure_function.assignAt(distances,name,value)
            return
      raise RuntimeError(name,"No se pudo asignar. Var no encontrada.")
      #self.ancestor(distance).values.append(name.valor,value)

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
 
