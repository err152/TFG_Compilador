from Token import Token,TokenType
import expressions
#import statements

class LoxRuntimeError(RuntimeError):
   token = None

   def __init__(token:Token, msg:str):
      super(msg)
      self.token = token

class Interprete(expressions.Visitor): #,statements.Visitor

   def stringify(self, obj:any) -> str:
      if obj == None:
         return None
      if is_number(obj):
         text = str(obj)
         if text.endsWith(".0"):
            text = text[0:len(text)-2]
         return text
      return str(obj)

   def interpret(self,expression:expressions.Expr):
      try:
         value = self.evaluate(expression)
         print(stringify(value))
      except RuntimeError as error:
         Lox.runtimeError(error)
      #except error:
         #print("Lox.runtimeError") # Provisional
         
   # Modificación post-Statements
   '''
   def interpret(self,statements:statements.Stmt):
      try:
         for statement in statements:
            self.execute(statement)
      except RuntimeError as error:
         Lox.runtimeError(error)
   '''

   def check_number_operand(operator: Token, operand: any):
      if self.is_number(operand):
         return
      raise LoxRuntimeError(operator,"Operand must be a number.")

   def check_number_operands(operator: Token, left: any, right: any):
      if is_number(left) and is_number(right):
         return
      raise LoxRuntimeError(operator,"Operands must be numbers.")
      
   def is_equal(a: any, b: any) -> bool:
      return a == b

   def is_number(obj: any) -> bool:
      return isinstance(obj,(int,float))

   def is_truthy(obj: any) -> bool:
      return bool(obj)

   def evaluate(self,expr: expressions.Expr):
      return expr.acepta(self)

   # Modificacion post_Statements
   '''
   def execute(self,stmt: statements.Stmt):
      stmt.accept(self)

   def visit_expression_stmt(self,stmt: statements.Expression):
      evaluate(stmt.expression)
      return None

   def visit_print_stmt(self,stmt: statements.Print):
      value = evaluate(stmt.expression)
      print(self.stringify(value))
      return None
      '''

   def visit_literal_expr(self,expr: expressions.Literal):
      return expr.valor

   def visit_grouping_expr(self,expr: expressions.Grouping):
      return evaluate(expr.expression)  

   def visit_unary_expr(self, expr: expressions.Unary):
      right = evaluate(expr.right)

      match expr.operator.type:
         case "MINUS":
            check_number_operand(expr.operator,right)
            return -right
         case "BANG":
            return not self.is_truthy(right)

      ## Unreachable
      return None
 
   def visit_binary_expr(self, expr: expressions.Binary):
      left = evaluate(expr.left)
      right = evaluate(expr.right)

      match expr.operator.type:
         case "BANG_EQUAL":
            return not self.is_equal(left,right)
         case "EQUAL_EQUAL":
            return self.is_equal(left,right)
         case "GREATER":
            check_number_operands(expr.operator,left,right)
            return left > right
         case "GREATER_EQUAL":
            check_number_operands(expr.operator,left,right)
            return left >= right
         case "LESS":
            check_number_operands(expr.operator,left,right)
            return left < right
         case "LESS_EQUAL":
            check_number_operands(expr.operator,left,right)
            return left <= right
         case "MINUS":
            check_number_operands(expr.operator,left,right)
            return left - right
         case "PLUS":
            if ((isinstance(left,str) and isinstance(right,str))
                or (self.is_number(left) and self.is_number(right))):
                return left + right
            raise LoxRuntimeError(expr.operator,"Operands must be two numbers or two strings.")
         case "SLASH":
            check_number_operands(expr.operator,left,right)
            return left / right
         case "STAR":
            check_number_operands(expr.operator,left,right)
            return left * right
         

      ## Unreachable
      return None

         
