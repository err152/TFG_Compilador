from Token import Token,TokenType
from Entorno import Entorno
from typing import List
import expressions
import statements
import copy

class LoxRuntimeError(RuntimeError):
   token = None

   def __init__(self,token:Token, msg:str):
      super().__init__(msg)
      self.token = token

class Interprete(expressions.ExprVisitor,statements.StmtVisitor):

   def __init__(self):
      self.ent = Entorno()
   
   def stringify(self, obj:any) -> str:
      if obj == None:
         return None
      if self.is_number(obj):
         text = str(obj)
         if text.endswith(".0"):
            text = text[0:len(text)-2]
         return text
      return str(obj)

   '''
   def interpret(self,expression:expressions.Expr):
      try:
         value = self.evaluate(expression)
         print(self.stringify(value))
      except LoxRuntimeError as error:
         print(error)
      #except error:
         #print("Lox.runtimeError") # Provisional
   ''' 
   # Modificación post-Statements
   
   def interpret(self,statements:List[statements.Stmt]):
      try:
         #print("declaraciones :::",statements)
         for statement in statements:
            self.execute(statement)
      except RuntimeError as error:
         raise RuntimeError(error)
   

   def check_number_operand(self, operator: Token, operand: any):
      #print("operator : ",operator," operand : ",operand)
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
      #print("::::::: obj = ",obj," de tipo ",type(obj))
      try:
         float(obj)
         return True
      except ValueError:
         return False
      #return isinstance(obj,(int,float))

   def is_truthy(self, obj: any) -> bool:
      return bool(obj)

   def evaluate(self,expr: expressions.Expr):
      return expr.acepta(self)

   # Modificacion post_Statements
   
   def execute(self,stmt: statements.Stmt):
      #print("declaracion ::: ",stmt)
      stmt.acepta(self)

   def executeBlock(self,state:List[statements.Stmt],ento:Entorno):
    previous = tuple(self.ent.values.items()) #copy.deepcopy(self.ent) # Guardo el entorno anterior
    #print("#######", previous)
    try:
        self.ent = ento 
        #print("Before execution:")
        for stat in state:
            self.execute(stat)
        #print("After execution:")
    finally:
      #print('#------#', previous)
      self.ent.values = dict(previous)

   def visit_block_stmt(self,stmt: statements.Block):
      #print("Dentro visit_block_stmt")
      self.executeBlock(stmt.statements, Entorno(self.ent))
      return None

   def visit_expression_stmt(self,stmt: statements.Expression):
      #print("dentro visit_expression_stmt")
      value = self.evaluate(stmt.expression)
      return None

   def visit_print_stmt(self,stmt: statements.Print):
      #print("Dentro visit_print_stmt")
      value = self.evaluate(stmt.expression)
      print(self.stringify(value))
      return None

   def visit_var_stmt(self,stmt: statements.Var):
      #print("Dentro visit_var_stmt")
      value : any = None
      if stmt.initializer is not None:
         #print("Dentro valor")
         value = self.evaluate(stmt.initializer)
         
      self.ent.define(stmt.name.valor,value)
      return None

   def visit_assign_expr(self,expr:expressions.Assign):
      value : any = self.evaluate(expr.value)
      self.ent.assign(expr.name,value)
      return value

   def visit_literal_expr(self,expr: expressions.Literal):
      return expr.value

   def visit_grouping_expr(self,expr: expressions.Grouping):
      return self.evaluate(expr.expression)  

   def visit_unary_expr(self, expr: expressions.Unary):
      right = self.evaluate(expr.right)
      #print("::: right = ",right,type(right))

      match expr.operator.tipo:
         case TokenType.MINUS:
            #print("operator : ",expr.operator)
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
      #print("::: left = ",left)
      right = self.evaluate(expr.right)
      #print("::: right = ",right)

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

         
