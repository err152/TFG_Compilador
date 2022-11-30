# test_lexer.py

import lexer
import unittest

class TestLexer(unittest.TestCase):
    
    def test_singleChars(self):
        a = lexer.Lexer('{ / *')
        b = str(self.extrae_tokens(a))
        assert b == "[Token(linea=0, tipo='LEFT_BRACE', valor='{'), Token(linea=0, tipo=None, valor='/'), Token(linea=0, tipo='STAR', valor='*')]"

    def test_multiChars(self):
        a = lexer.Lexer('== > !=')
        b = str(self.extrae_tokens(a))
        assert b == "[Token(linea=0, tipo='EQUAL_EQUAL', valor='=='), Token(linea=0, tipo='GREATER', valor='>'), Token(linea=0, tipo='BANG_EQUAL', valor='!=')]"

    def test_comment(self):
        a = lexer.Lexer(' Hola //Esto es un comentario \n Holaa')
        b = str(self.extrae_tokens(a))
        assert b == '[Token(linea=0, tipo='IDENTIFICADOR', valor='Hola'), Token(linea=1, tipo='IDENTIFICADOR', valor='Holaa')]'

    def test_espacio(self):
        a = lexer.Lexer('"espacio " 32 \ne2p4c10 ')
        b = str(self.extrae_tokens(a))
        assert b == '[Token(linea=0, tipo='STRING', valor='"espacio "'), Token(linea=0, tipo='NUMERO', valor='32'), Token(linea=1, tipo='IDENTIFICADOR', valor='e2p4c10')]'

    def test_string(self):
        a = lexer.Lexer('"string _ 34 */' ' " check')
        b = str(self.extrae_tokens(a))
        assert b == '[[0,"STRING","string _ 34 */ "], [0,"IDENTIFICADOR",check]]'
        c = lexer.Lexer(' "" " " ')
        d = str(self.extrae_tokens(c))
        assert d == '[[0,"STRING",""], [0,"STRING"," "]]'
        
    def test_numero(self):
        a = lexer.Lexer(' 2 2345 2.356 2. ')
        b = str(self.extrae_tokens(a))
        assert b == '[[0,"NUMERO",2], [0,"NUMERO",2345], [0,"NUMERO",2.356]]'

    def test_id(self):
        a = lexer.Lexer(' true false and adn burrito')
        b = str(self.extrae_tokens(a))
        print("---------------------",b)
        assert b == '[[0,"TRUE",true], [0,"FALSE",false], [0,"AND",and], [0,"IDENTIFICADOR",adn], [0,"IDENTIFICADOR",burrito]]'

    def test_total(self):
        a = lexer.Lexer('''class Brunch < Breakfast {
           init(meat, bread, drink) {
               super.init(meat, bread);
               this.drink = drink;
               }
           }''')
        b = str(self.extrae_tokens(a))
        assert b == '''[[0,"CLASS",class], [0,"IDENTIFICADOR",Brunch], [0,"LESS",<], [0,"IDENTIFICADOR",Breakfast], [1,"LEFT_BRACE",{], [1,"IDENTIFICADOR",init], [1,"LEFT_PAREN",(], [1,"IDENTIFICADOR",meat], [1,"COMMA",,], [1,"IDENTIFICADOR",bread], [1,"COMMA",,], [1,"IDENTIFICADOR",drink], [1,"RIGHT_PAREN",)], [2,"LEFT_BRACE",{], [2,"SUPER",super], [2,"DOT",.], [2,"IDENTIFICADOR",init], [2,"LEFT_PAREN",(], [2,"IDENTIFICADOR",meat], [2,"COMMA",,], [2,"IDENTIFICADOR",bread], [2,"RIGHT_PAREN",)], [3,"SEMICOLON",;], [3,"THIS",this], [3,"DOT",.], [3,"IDENTIFICADOR",drink], [3,"EQUAL",=], [3,"IDENTIFICADOR",drink], [4,"SEMICOLON",;], [5,"RIGHT_BRACE",}], [5,"RIGHT_BRACE",}]]'''

    def extrae_tokens(self,a):
        l = []
        for i in a.devolver_tokens():
            l.append(i)
        return l
        
                           
if __name__ == '__main__':
    unittest.main()
