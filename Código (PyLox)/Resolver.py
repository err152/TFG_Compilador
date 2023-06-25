import expressions
import statements
from enum import Enum
from Token import Token
from Interprete import Interprete
from typing import List

class FunctionType(Enum):
      NONE = 'NONE'
      FUNCTION = 'FUNCTION'
      INITIALIZER = 'INITIALIZER'
      METHOD = 'METHOD'
      
class ClassType(Enum):
      NONE = 'NONE'
      CLASS = 'CLASS'

class Resolver(expressions.ExprVisitor,statements.StmtVisitor):
   
   def __init__(self,inter: Interprete):
      self.inter = inter
      self.scopes = [{}]
      self.currentFunction = FunctionType.NONE
      self.currentClass = ClassType.NONE
   
   def resolve(self, *args, **kwargs):
      if 'statements' in kwargs:
         statements = kwargs['statements']
         for stat in statements:
            self.resolve(statement=stat)
      elif 'statement' in kwargs:
         statement = kwargs['statement']
         statement.acepta(self)
      elif 'expression' in kwargs:
         expression = kwargs['expression']
         expression.acepta(self)
         
   def resolveFunction(self, func:statements.Function, typee:FunctionType):
      enclosingFunction : FunctionType = self.currentFunction
      self.currentFunction = typee
      
      self.beginScope()
      for param in func.params:
         self.declare(param)
         self.define(param)
      self.resolve(statements=func.body)
      self.endScope()
      
      self.currentFunction = enclosingFunction
      
   def visit_if_stmt(self, stmt:statements.If):
      self.resolve(statement=stmt.condition)
      self.resolve(statement=stmt.thenBranch)
      if stmt.elseBranch is not None:
         self.resolve(statement=stmt.elseBranch)
      return None
   
   def visit_print_stmt(self, stmt:statements.Print):
      self.resolve(statement=stmt.expression)
      return None
   
   def visit_return_stmt(self, stmt:statements.Return):
      if self.currentFunction == FunctionType.NONE:
         raise RuntimeError(stmt.keyword,"Can't return from top-level code.")
         #lox.error(stmt.keyword,"Can't return from top-level code.")
      if stmt.value is not None:
         if self.currentFunction == FunctionType.INITIALIZER:
            raise RuntimeError(stmt.keyword,"Can't return a value from an initializer.")
         self.resolve(statement=stmt.value)
      return None
         
   def beginScope(self):
      self.scopes.append(dict())
      
   def endScope(self):
      self.scopes.pop()
      
   def declare(self,name:Token):
      if len(self.scopes) == 0:
         return
      scope = self.scopes[-1] # peek()
      if name.valor in scope:
         raise RuntimeError(name,"Already a variable with this name in this scope.")
         #mport lox
         #lox.error(name,"Already a variable with this name in this scope.")
      scope[name.valor] = False
      
   def define(self,name:Token):
      if len(self.scopes) == 0:
         return
      self.scopes[-1][name.valor] = True
      
   def resolveLocal(self, expr:expressions.Expr, name:Token):
      i = len(self.scopes) - 1
      while i >= 0:
         if name.valor in self.scopes[i]:
            self.inter.resolve(expr,len(self.scopes)-1-i)
            return
         i = i-1
      
   def visit_block_stmt(self, stmt:statements.Block):
      self.beginScope()
      self.resolve(statements=stmt.statements)
      self.endScope()
      return None
   
   def visit_class_stmt(self,stmt: statements.Class):
      enclosingClass : ClassType = self.currentClass
      self.currentClass = ClassType.CLASS
      
      self.declare(stmt.name)
      self.define(stmt.name)
      
      self.beginScope()
      self.scopes[-1]["this"] = True
      
      for method in stmt.methods:
         declaration : FunctionType = FunctionType.METHOD
         if method.name.valor == "init":
            declaration = FunctionType.INITIALIZER
         self.resolveFunction(method, declaration)
         
      self.endScope()
      
      self.currentClass = enclosingClass
         
      return None
   
   def visit_expression_stmt(self, stmt:statements.Expr):
      self.resolve(statement=stmt.expression)
      return None
   
   def visit_function_stmt(self, stmt:statements.Function):
      self.declare(stmt.name)
      self.define(stmt.name)
      
      self.resolveFunction(stmt, FunctionType.FUNCTION)
      return None
         
   def visit_var_stmt(self, stmt:statements.Var):
      self.declare(stmt.name)
      if stmt.initializer is not None:
         self.resolve(statement=stmt.initializer)
      self.define(stmt.name)
      return None
   
   def visit_while_stmt(self, stmt:statements.While):
      self.resolve(statement=stmt.condition)
      self.resolve(statement=stmt.body)
      return None
   
   def visit_assign_expr(self, expr:expressions.Assign):
      self.resolve(expression=expr.value)
      self.resolveLocal(expr,expr.name)
      return None
   
   def visit_binary_expr(self, expr:expressions.Binary):
      self.resolve(expression=expr.left)
      self.resolve(expression=expr.right)
      return None
   
   def visit_call_expr(self, expr:expressions.Call):
      self.resolve(expression=expr.callee)
      for argu in expr.arguments:
         self.resolve(expression=argu)
      return None
   
   def visit_get_expr(self, expr:expressions.Get):
      self.resolve(expr.object)
      return None
   
   def visit_grouping_expr(self, expr:expressions.Grouping):
      self.resolve(expression=expr.expression)
      return None
   
   def visit_literal_expr(self, expr:expressions.Literal):
      return None
   
   def visit_logical_expr(self, expr:expressions.Logical):
      self.resolve(expression=expr.left)
      self.resolve(expression=expr.right)
      return None
   
   def visit_set_expr(Self, expr:expressions.Set):
      self.resolve(expr.value)
      self.resolve(expr.object)
      return None
   
   def visit_this_expr(self, expr:expressions.This):
      if self.currentClass == ClassType.NONE:
         raise RuntimeError(expr.keyword, "Can't use 'this' outside of a class.")
      self.resolveLocal(expr,expr.keyword)
      return None
   
   def visit_unary_expr(self, expr:expressions.Unary):
      self.resolve(expression=expr.right)
      return None
   
   def visit_variable_expr(self, expr:expressions.Variable):
      if not len(self.scopes) == 0:
         try:
            a = self.scopes[-1][expr.name.valor]
            if a == False:
               raise RuntimeError(expr.name,"Can't read local variable in its own initializer.")
               # no se si está bien 
         except KeyError:
            pass
            #lox.error(expr.name,"Can't read local variable in its own initializer.")
         
      self.resolveLocal(expr,expr.name)
      return None
   
   