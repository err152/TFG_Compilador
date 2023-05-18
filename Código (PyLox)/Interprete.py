from Token import Token,TokenType
from Entorno import Entorno
from typing import List
from Return import Return
#import LoxCallable
import expressions
import statements

class LoxRuntimeError(RuntimeError):
   token = None

   def __init__(self,token:Token, msg:str):
      super().__init__(msg)
      self.token = token

class Interprete(expressions.ExprVisitor,statements.StmtVisitor):

   def __init__(self):
      self.ent = Entorno()
   
   def stringify(self, obj:any) -> str:
      from LoxFunction import LoxFunction
      if obj == None:
         return None
      if self.is_number(obj):
         text = str(obj)
         if text.endswith(".0"):
            text = text[0:len(text)-2]
         return text
      return str(obj)
   
   def interpret(self,statements:List[statements.Stmt]):
      try:
         for statement in statements:
            self.execute(statement)
      except RuntimeError as error:
         raise RuntimeError(error)

   def check_number_operand(self, operator: Token, operand: any):
      if self.is_number(operand):
         return
      raise LoxRuntimeError(operator,"Operand must be a number.")

   def check_number_operands(self, operator: Token, left: any, right: any):
      if self.is_number(left) and self.is_number(right):
         return
      raise LoxRuntimeError(operator,"Operands must be numbers.")
      
   def is_equal(self, a: any, b: any) -> bool:
      return a == b

   def is_number(self, obj: any) -> bool:
      try:
         float(obj)
         return True
      except (ValueError,TypeError):
         return False

   def is_truthy(self, obj: any) -> bool:
      if obj == "0":
         return False
      return bool(obj)

   def evaluate(self,expr: expressions.Expr):
      return expr.acepta(self)
   
   def execute(self,stmt: statements.Stmt):
      stmt.acepta(self)

   def executeBlock(self,state:List[statements.Stmt]):
      self.ent.enter_scope()
      try:
        for stat in state:
            self.execute(stat)
      finally:
         
         self.ent.exit_scope()

   def visit_block_stmt(self,stmt: statements.Block):
      self.executeBlock(stmt.statements)
      return None

   def visit_expression_stmt(self,stmt: statements.Expression):
      value = self.evaluate(stmt.expression)
      return None
   
   def visit_function_stmt(self,stmt:statements.Function):
      from LoxFunction import LoxFunction
      funct : LoxFunction = LoxFunction(stmt,self.ent)
      self.ent.define(stmt.name.valor, funct)
      return None

   def visit_if_stmt(self, stmt: statements.If):
      if self.is_truthy(self.evaluate(stmt.condition)):
         self.execute(stmt.thenBranch)
      elif stmt.elseBranch is not None:
         self.execute(stmt.elseBranch)
      return None

   def visit_print_stmt(self,stmt: statements.Print):
      value = self.evaluate(stmt.expression)
      print(self.stringify(value))
      return None
   
   def visit_return_stmt(self, stmt:statements.Return):
      value = None
      if stmt.value is not None:
         value = self.evaluate(stmt.value)
         
      raise Return(value)

   def visit_var_stmt(self,stmt: statements.Var):
      value : any = None
      if stmt.initializer is not None:
         value = self.evaluate(stmt.initializer)
         
      self.ent.define(stmt.name.valor,value)
      return None

   def visit_while_stmt(self,stmt: statements.While):
      while self.is_truthy(self.evaluate(stmt.condition)):
         self.execute(stmt.body)

      return None

   def visit_assign_expr(self,expr:expressions.Assign):
      value : any = self.evaluate(expr.value)
      self.ent.assign(expr.name,value)
      return value

   def visit_literal_expr(self,expr: expressions.Literal):
      return expr.value

   def visit_logical_expr(self,expr: expressions.Logical):
      left = self.evaluate(expr.left)
      if expr.operator.tipo == TokenType.OR:
         if self.is_truthy(left):
            return left
      elif not self.is_truthy(left):
         return False # left
      
      x = self.evaluate(expr.right)
      if x == None or x == "0":
         return False
      else:
         return x

   def visit_grouping_expr(self,expr: expressions.Grouping):
      return self.evaluate(expr.expression)  

   def visit_unary_expr(self, expr: expressions.Unary):
      right = self.evaluate(expr.right)

      match expr.operator.tipo:
         case TokenType.MINUS:
            self.check_number_operand(expr.operator,right)
            return -float(right)
         case TokenType.BANG:
            return not self.is_truthy(right)

      ## Unreachable
      return None

   def visit_variable_expr(self,expr:expressions.Variable):
      return self.ent.get(expr.name)
 
   def visit_binary_expr(self, expr: expressions.Binary):
      left = self.evaluate(expr.left)
      right = self.evaluate(expr.right)

      match expr.operator.tipo:
         case TokenType.BANG_EQUAL:
            return not self.is_equal(left,right)
         case TokenType.EQUAL_EQUAL:
            return self.is_equal(left,right)
         case TokenType.GREATER:
            self.check_number_operands(expr.operator,left,right)
            return float(left) > float(right)
         case TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator,left,right)
            return float(left) >= float(right)
         case TokenType.LESS:
            self.check_number_operands(expr.operator,left,right)
            return float(left) < float(right)
         case TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator,left,right)
            return float(left) <= float(right)
         case TokenType.MINUS:
            self.check_number_operands(expr.operator,left,right)
            return float(left) - float(right)
         case TokenType.PLUS:
            if self.is_number(left) and self.is_number(right):
               return float(left) + float(right)
            elif isinstance(left,str) and isinstance(right,str):
               return left[0:-1] + right[1::]
            raise LoxRuntimeError(expr.operator,"Operands must be two numbers or two strings.")
         case TokenType.SLASH:
            self.check_number_operands(expr.operator,left,right)
            return float(left) / float(right)
         case TokenType.STAR:
            self.check_number_operands(expr.operator,left,right)
            return float(left) * float(right)
         

      ## Unreachable
      return None

   def visit_call_expr(self, expr: expressions.Call):
      from LoxCallable import LoxCallable # Inside import
      from LoxFunction import LoxFunction
      callee : any = self.evaluate(expr.callee)

      arguments : List[any] = []
      for argument in expr.arguments:
         arguments.append(self.evaluate(argument))

      if not isinstance(callee, LoxCallable):
         raise RuntimeError(expr.paren,"Can only call functions and classes.")
      
      function : LoxCallable
      if isinstance(callee, LoxFunction):
         function = callee
      else:
         function = cast(LoxCallable, callee)
      if len(arguments) is not function.arity():
         raise RuntimeError(expr.paren,"Expected "+function.arity()+
         " arguments but got "+len(arguments)+".")

      return function.call(self,arguments)

         
