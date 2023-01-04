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


class Expr(ABC):
   @abstractmethod
   def acepta(Visitor):
       pass

class Binary(Expr):
   def __init__(self,left:Expr,operator:Token,right:Expr):
       self.left = left
       self.operator = operator
       self.right = right

   def acepta(self, visitor: Visitor):
       return visitor.visit_binary_expr(self)

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

class Unary(Expr):
   def __init__(self,operator:Token,right:Expr):
       self.operator = operator
       self.right = right

   def acepta(self, visitor: Visitor):
       return visitor.visit_unary_expr(self)

