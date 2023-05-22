##### Para ejecutar por fichero copiar
## 'C:\\Users\\Eduardo\\Desktop\\Universidad\\2o Cuatri\\TFG_compilador\\Código (PyLox)\\b4sur4\\lox_prueba.lox'

from pathlib import Path
from sys import argv

from parser import Parser
from lexer import Lexer
from Interprete import Interprete,LoxRuntimeError
from Token import Token,TokenType
import AstPrinter
from Resolver import Resolver

class Lox:
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

    def run(source:str):
        lex = Lexer(source)
        tokens = lex.extrae_tokens()

        pars = Parser(tokens)
        stmts = pars.parse()
                
        inter = Interprete()
        
        #res = Resolver(inter)
        #res.resolve(statements=stmts)
        #if self.hadError:
        #    return
        
        inter.interpret(stmts)
    

    def runFile(path:str):
        with open(path,'r') as archivo:
            data = archivo.read()
        Lox.run(data)

        if Lox.hadError:
            exit(65)
        if Lox.hadRuntimeError:
            exit(70)

        Lox.hadError = False

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
    
    Lox.runFile('C:\\Users\\Eduardo\\Desktop\\Universidad\\2o Cuatri\\TFG_compilador\\Código (PyLox)\\b4sur4\\prueba_func9.lox')
    '''
    if len(args) > 1:
        print("Usage: jlox [script]")
        exit(65)
        
    elif len(args) == 1:
        Lox.runFile(args[0])

    else:
        Lox.runPrompt()
    '''
    
main(argv[1:])

