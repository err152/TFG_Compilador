from Token import Token,TokenType
import expressions

class LoxRuntimeError(RuntimeError):
   token = None

   def __init__(token:Token, msg:str):
      super(msg)
      self.token = token

class Interprete(expressions.Visitor):

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
         value = evaluate(expression)
         print(stringify(value))
      except:
         print("Lox.runtimeError") # Provisional

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

   def evaluate(expr: expressions.Expr):
      return expr.accept(self)

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

         
