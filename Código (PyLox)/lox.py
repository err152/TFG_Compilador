from pathlib import Path

from parser import ParseError
import lexer
from Token import Token,TokenType
import AstPrinter

hadError = False

def report(self,linea:int,where:str,msg:str):
    print(f"[linea {linea}] Error{where}: {msg}")
    self.hadError = true

def error(self,token:Token,msg:str):
    if token.tipo == TokenType.EOF:
        self.report(token.linea, " at end",msg)
    else:
        self.report(token.linea," at '"+token.value+"'",msg)
    

def run(self,source:str):
    '''
    lex = Lexer(source)
    tokens = lex.scanTokens()

    for token in tokens:
        print(token)
    '''

    parser = Parser(tokens)
    expression = parser.parse()

    if self.hadError:
        exit(65)
    
    print(AstPrinter().print(expression))

def runFile(self,path:str):
    data = path.read_text(encoding='utf-8',errors='strict')
    self.run(data)

    if self.hadError:
        exit(65)

    self.hadError = false

def runPrompt(self):
    while True:
        print("> ")
        line = input()
        if line == None:
            return
        else:
            self.run(line)

    self.hadError = false


def main(self,*args):
    if len(*args) > 1:
        print("Usage: jlox [script]")
        exit(65)
        
    elif len(*args) == 1:
        self.runFile(args[0])

    else:
        self.runPrompt()
        
if __name__ == "__main__":
    main()
