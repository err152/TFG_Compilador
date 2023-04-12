from pathlib import Path
from sys import argv

from parser import Parser
from lexer import Lexer
#from Interprete import Interprete,LoxRuntimeError
from Token import Token,TokenType
import AstPrinter

class Lox:
    #interpreter = Interprete()
    hadError = False
    hadRuntimeError = False

    def report(linea:int,where:str,msg:str):
        print(f"[linea {linea}] Error{where}: {msg}")
        Lox.hadError = true

    def error(token:Token,msg:str):
        if token.tipo == TokenType.EOF:
            Lox.report(token.linea, " at end",msg)
        else:
            Lox.report(token.linea," at '"+token.value+"'",msg)

    #def runtimeError(error:LoxRuntimeError):
        #print(f"{error.message}\n[line {error.token.linea}]")
        #Lox.hadRuntimeError = true

    def run(source:str):
        lex = Lexer(source)
        tokens = lex.extrae_tokens()
        print(f"-- tokens : {tokens}")
    
        '''
        for token in tokens:
            print(token)
        '''

        pars = Parser(tokens)
        print(f"-- tokens in parser : {pars.tokens}")
        expr = pars.parse()
        #stmts = pars.parse()
        print(f"-- expr : {expr}")

        #Lox.interpreter.interpret(expr)
        #Lox.interpreter.interpret(stmts)
    
        print(AstPrinter.AstPrinter().print(expr))

    def runFile(path:str):
        data = path.read_text(encoding='utf-8',errors='strict')
        Lox.run(data)

        if Lox.hadError:
            exit(65)
        if Lox.hadRuntimeError:
            exit(70)

        Lox.hadError = false

    def runPrompt():
        while True:
            print("> ")
            line = input()
            if line == None:
                return
            else:
                Lox.run(line)

        Lox.hadError = false


def main(args):
    if len(args) > 1:
        print("Usage: jlox [script]")
        exit(65)
        
    elif len(args) == 1:
        Lox.runFile(args[0])

    else:
        Lox.runPrompt()
        
main(argv[1:])
