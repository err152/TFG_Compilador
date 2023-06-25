##### Para ejecutar por fichero copiar
## 'C:\\Users\\Eduardo\\Desktop\\Universidad\\2o Cuatri\\TFG_compilador\\Código (PyLox)\\b4sur4\\lox_prueba.lox'

from pathlib import Path
from sys import argv

from parser import Parser
from lexer import Lexer
from Interprete import Interprete,LoxRuntimeError
from Token import Token,TokenType
from AstPrinter import AstPrinter
from Resolver import Resolver

class Lox:
    hadError = False
    hadRuntimeError = False

    def report(self, linea:int,where:str,msg:str):
        print(f"[linea {linea}] Error{where}: {msg}")
        self.hadError = true

    def error(self, token:Token,msg:str):
        if token.tipo == TokenType.EOF:
            self.report(token.linea, " at end",msg)
        else:
            self.report(token.linea," at '"+token.value+"'",msg)

    def run(self, source:str, inter : Interprete = None):
        lex = Lexer(source)
        tokens = lex.extrae_tokens()

        pars = Parser(tokens)
        stmts = pars.parse()
        
        #printer = AstPrinter()
        #print(printer.print_extended(stmts))  
                          
        res = Resolver(inter)
        res.resolve(statements=stmts)
        if self.hadError:
            return
        
        return inter.interpret(stmts)
    

    def runFile(self, path:str):
        inter = Interprete()
        with open(path,'r') as archivo:
            data = archivo.read()
        self.run(data,inter)

        if self.hadError:
            exit(65)
        if self.hadRuntimeError:
            exit(70)

        self.hadError = False

    def runPrompt(self):
        inter = Interprete()
        while True:
            print("> ")
            line = input()
            if line == None:
                return
            else:
                self.run(line,inter)

        self.hadError = false

def main(args):
    a = Lox()
    
    a.runFile('C:\\Users\\Eduardo\\Desktop\\Universidad\\2o Cuatri\\TFG_compilador\\Código (PyLox)\\pruebas\\prueba_0.lox')
    '''
    if len(args) > 1:
        print("Usage: jlox [script]")
        exit(65)
        
    elif len(args) == 1:
        a.runFile(args[0])
        
    else:
        a.runPrompt()
    '''
#main(argv[1:])

