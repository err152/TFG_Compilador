import expressions
from Token import Token, TokenType

class AstPrinter(expressions.Visitor):
   
   def print(self, expr:expressions.Expr) -> str:
      return expr.acepta(self)

   def parenthesize(self, name:str, *exprs: expressions.Expr) -> str:
      result = " ".join(expr.acepta(self) for expr in exprs)
      return f"({name} {result})"

   def visit_binary_expr(self, expr:expressions.Binary) -> str:
      return self.parenthesize(expr.operator.valor, expr.left, expr.right)

   def visit_grouping_expr(self, expr:expressions.Grouping) -> str:
      return self.parenthesize("group", expr.expression)

   def visit_literal_expr(self, expr:expressions.Literal) -> str:
      if expr.value == None:
         return "nil"
      
      return str(expr.value)

   def visit_unary_expr(self, expr:expressions.Unary) -> str:
      return self.parenthesize(expr.operator.valor, expr.right)


if __name__ == "__main__":
   exp = expressions.Binary(
      expressions.Unary(
         Token(1,TokenType.MINUS,"-"),
         expressions.Literal(123)
         ),
      Token(1,TokenType.STAR,"*"),
      expressions.Grouping(expressions.Literal(45.67))
      )

   print(AstPrinter().print(exp))                      
   
