'''from Token import Token
from typing import Any
from abc import ABC, abstractmethod

class Visitor(ABC):
   @abstractmethod
   def visit_expression_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_print_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_var_stmt(self, stmt: 'Stmt'):
       pass


class Stmt(ABC):
   @abstractmethod
   def acepta(Visitor):
       pass

class Expression(Stmt):
   def __init__(self,expression:Expr):
       self.expression = expression

   def acepta(self, visitor: Visitor):
       return visitor.visit_expression_stmt(self)

class Print(Stmt):
   def __init__(self,expression:Expr):
       self.expression = expression

   def acepta(self, visitor: Visitor):
       return visitor.visit_print_stmt(self)

class Var(Stmt):
   def __init__(self,name:Token,initializer:Expr):
       self.name = name
       self.initializer = initializer

   def acepta(self, visitor: Visitor):
       return visitor.visit_var_stmt(self)
'''
