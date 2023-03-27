from Token import Token
from typing import Any
from abc import ABC, abstractmethod

class Visitor(ABC):
   @abstractmethod
   def visit_binary_expr(self, expr: 'Expr'):
       pass

   @abstractmethod
   def visit_grouping_expr(self, expr: 'Expr'):
       pass

   @abstractmethod
   def visit_literal_expr(self, expr: 'Expr'):
       pass

   @abstractmethod
   def visit_unary_expr(self, expr: 'Expr'):
       pass

   @abstractmethod
   def visit_variable_expr(self, expr: 'Expr'):
       pass


class Expr(ABC):
   @abstractmethod
   def acepta(Visitor):
       pass

   def __repr__(self):
      return str(type(self))

class Binary(Expr):
   def __init__(self,left:Expr,operator:Token,right:Expr):
       self.left = left
       self.operator = operator
       self.right = right

   def acepta(self, visitor: Visitor):
       return visitor.visit_binary_expr(self)

   def __repr__(self):
      return str(self.left)+str(self.operator)+str(self.right)

class Grouping(Expr):
   def __init__(self,expression:Expr):
       self.expression = expression

   def acepta(self, visitor: Visitor):
       return visitor.visit_grouping_expr(self)

class Literal(Expr):
   def __init__(self,value:Any):
       self.value = value

   def acepta(self, visitor: Visitor):
       return visitor.visit_literal_expr(self)

   def __repr__(self):
      return str(self.value)

class Unary(Expr):
   def __init__(self,operator:Token,right:Expr):
       self.operator = operator
       self.right = right

   def acepta(self, visitor: Visitor):
       return visitor.visit_unary_expr(self)

class Variable(Expr):
   def __init__(self,name:Token):
       self.name = name

   def acepta(self, visitor: Visitor):
       return visitor.visit_variable_expr(self)

