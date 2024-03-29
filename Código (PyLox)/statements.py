from Token import Token
from typing import Any
from abc import ABC, abstractmethod
from typing import List
from expressions import Expr

class StmtVisitor(ABC):
   @abstractmethod
   def visit_block_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_class_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_expression_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_function_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_if_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_print_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_return_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_var_stmt(self, stmt: 'Stmt'):
       pass

   @abstractmethod
   def visit_while_stmt(self, stmt: 'Stmt'):
       pass


class Stmt(ABC):
   @abstractmethod
   def acepta(StmtVisitor):
       pass

class Block(Stmt):
   def __init__(self,statements:List[Stmt]):
       self.statements = statements

   def acepta(self, visitor: StmtVisitor):
       return visitor.visit_block_stmt(self)

class Class(Stmt):
   def __init__(self,name:Token,methods:List[Stmt]):
       self.name = name
       self.methods = methods

   def acepta(self, visitor: StmtVisitor):
       return visitor.visit_class_stmt(self)

class Expression(Stmt):
   def __init__(self,expression:Expr):
       self.expression = expression

   def acepta(self, visitor: StmtVisitor):
       return visitor.visit_expression_stmt(self)

class Function(Stmt):
   def __init__(self,name:Token,params:List[Token],body:List[Stmt]):
       self.name = name
       self.params = params
       self.body = body

   def acepta(self, visitor: StmtVisitor):
       return visitor.visit_function_stmt(self)

class If(Stmt):
   def __init__(self,condition:Expr,thenBranch:Stmt,elseBranch:Stmt):
       self.condition = condition
       self.thenBranch = thenBranch
       self.elseBranch = elseBranch

   def acepta(self, visitor: StmtVisitor):
       return visitor.visit_if_stmt(self)

class Print(Stmt):
   def __init__(self,expression:Expr):
       self.expression = expression

   def acepta(self, visitor: StmtVisitor):
       return visitor.visit_print_stmt(self)

class Return(Stmt):
   def __init__(self,keyword:Token,value:Expr):
       self.keyword = keyword
       self.value = value

   def acepta(self, visitor: StmtVisitor):
       return visitor.visit_return_stmt(self)

class Var(Stmt):
   def __init__(self,name:Token,initializer:Expr):
       self.name = name
       self.initializer = initializer

   def acepta(self, visitor: StmtVisitor):
       return visitor.visit_var_stmt(self)

class While(Stmt):
   def __init__(self,condition:Expr,body:Stmt):
       self.condition = condition
       self.body = body

   def acepta(self, visitor: StmtVisitor):
       return visitor.visit_while_stmt(self)

