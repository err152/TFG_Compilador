import expressions
import statements
from enum import Enum
from Token import Token
from Interprete import Interprete
from typing import List

class FunctionType(Enum):
      NONE = 'NONE'
      FUNCTION = 'FUNCTION'

class Resolver(expressions.ExprVisitor,statements.StmtVisitor):
   
   scopes = [[str,bool]]
   currentFunc = FunctionType.NONE
   
   def __init__(self,inter: Interprete):
      self.inter = inter
   
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
      enclosingFunction : FunctionType = self.currentFunc
      self.currentFunc = typee
      
      self.beginScope()
      for param in func.params:
         self.declare(param)
         self.define(param)
      self.resolve(func.body)
      self.endScope()
      
      self.currentFunc = enclosingFunction
      
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
         Lox.error(stmt.keyword,"Can't return from top-level code.")
      if stmt.value is not None:
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
         Lox.error(name,"Already a variable with this name in this scope.")
      scope.append([name.valor,False])
      
   def define(self,name:Token):
      if len(self.scopes) == 0:
         return
      self.scopes[-1].append([name.valor,True])
      
   def resolveLocal(expr:expressions.Expr, name:Token):
      i = len(self.scopes) - 1
      while i >= 0:
         if name.valor in self.scopes[i]:
            self.inter.resolve(expression=expr,jumps=len(self.scopes)-1-i) # esto no está bien
            return
         i = i-1
      
   def visit_block_stmt(self, stmt:statements.Block):
      self.beginScope()
      self.resolve(statements=stmt.statements)
      self.endScope()
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
   
   def visit_grouping_expr(self, expr:expressions.Grouping):
      self.resolve(expression=expr.expression)
      return None
   
   def visit_literal_expr(self, expr:expressions.Literal):
      return None
   
   def visit_logical_expr(self, expr:expressions.Logical):
      self.resolve(expression=expr.left)
      self.resolve(expression=expr.right)
      return None
   
   def visit_unary_expr(self, expr:expressions.Unary):
      self.resolve(expression=expr.right)
      return None
   
   def visit_variable_expr(self, expr:expressions.Variable):
      import Lox
      if not len(self.scopes) == 0 and self.scopes[-1][expr.name.valor] == False: # no se si está bien 
         Lox.error(expr.name,"Can't read local variable in tis own initializer.")
         
      self.resolveLocal(expr,expr.name)
      return None
   
   