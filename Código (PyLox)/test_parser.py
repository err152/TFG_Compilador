# test_parser.py
'''
import os
import sys
import re
import traceback
init()

DIRECTORIO = os.path.expanduser(r"C:\Users\Eduardo\Desktop\Universidad\2o Cuatri\TFG_compilador\Código (PyLox)")
sys.path.append(DIRECTORIO)

from parser import Parser
from Token import Token,TokenType

NUMLINEAS = 3
#sys.path.append(DIRECTORIO)
DIR = os.path.join(DIRECTORIO, 'test_pars_files')
FICHEROS = os.listdir(DIR)
TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(DIR, fich)) and
         re.search(r"^[a-zA-Z].*\.(lox|test|cl)$",fich)]
TESTS.sort()
TESTS = TESTS # ¿?

if True:
    for fich in TESTS:
        f = open(os.path.join(DIR, fich), 'r', newline='')
        g = open(os.path.join(DIR,fich + '.out'), 'r', newline='')
        if os.path.isfile(os.path.join(DIR, fich)+'.nuestro'):
            os.remove(os.path.join(DIR,fich)+'.nuestro')
        if os.path.isfile(os.path.join(DIR,fich)+'.bien'):
            os.remove(os.path.join(DIR, fich)+'.bien')
        texto = ''
        entrada = read()
        lexer = lexer(entrada)
        f.close()

        ## Parser test
        tokens = lexer.extrae_tokens
        parser = parser(tokens)
        #parser.nombre_fichero = fich
        #parser.errores = []
        bien = ''.join([c for c in g.readlines() if c and '#' not in c])
        g.close()
        j = parser.parse()
        try:
            if j != None: #and not parser.errores:
                try:
                    j.Tipo() # mis expresiones no tienen tipo?
                    resultado = '\n'.join([c for c in j.str(0).split('\n')
                                           if c and '#' not in c])
                except Exception as e:
                    resultado = f'{parser.nombre_fichero}:{str(e)}'
            else:
                resultado = '\n'.join(parser.errores)
                resultado += '\n' + "Compilation halted due to lex and parse errors"
            if resultado.lower().strip().split() != bien.lower().strip().split():
                    print(f"Revisa el fichero {fich}")
            
        except Exception as e:
            traceback.print_exc()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(f"Lanza excepción en {fich} con el texto {e}")
'''
class TestLexer(unittest.TestCase):
    
    def test_singleChars(self):
        pars = Parser([Token(0,TokenType.NUMBER,"1"), Token(0,"PLUS","+"), Token(0,"NUMBER","2")])
        print(f"-- tokens in parser : {pars.tokens}")
        expr = pars.parse()
        print(f"-- expr : {expr}")
        #assert b == '[[0,"NUMBER",1], [0,"PLUS",+], [0,"NUMBER",2]]'

                     
if __name__ == '__main__':
    unittest.main()
