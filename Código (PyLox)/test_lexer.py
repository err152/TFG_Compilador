# test_lexer.py

import lexer
import unittest

class TestLexer(unittest.TestCase):
    
    def test_singleChars(self):
        a = lexer.Lexer('{ / *')
        b = str(a.extrae_tokens())
        assert b == '''[Token(0,TokenType.LEFT_BRACE,"{"), Token(0,TokenType.None,"/"), Token(0,TokenType.STAR,"*")]'''

    def test_addition(self):
        a = lexer.Lexer('1+1')
        b = str(a.extrae_tokens())
        assert b == '''[Token(0,TokenType.NUMBER,"1"), Token(0,TokenType.PLUS,"+"), Token(0,TokenType.NUMBER,"1")]'''

    def test_multiChars(self):
        a = lexer.Lexer('== > !=')
        b = str(a.extrae_tokens())
        assert b == '''[Token(0,TokenType.EQUAL_EQUAL,"=="), Token(0,TokenType.GREATER,">"), Token(0,TokenType.BANG_EQUAL,"!=")]'''

    def test_comment(self):
        a = lexer.Lexer(' Hola //Esto es un comentario \n Holaa')
        b = str(a.extrae_tokens())
        assert b == '''[Token(0,TokenType.IDENTIFICADOR,"Hola"), Token(1,TokenType.IDENTIFICADOR,"Holaa")]'''

    def test_espacio(self):
        a = lexer.Lexer('"espacio " 32 \ne2p4c10 ')
        b = str(a.extrae_tokens())
        assert b == '''[Token(0,TokenType.STRING,""espacio ""), Token(0,TokenType.NUMBER,"32"), Token(1,TokenType.IDENTIFICADOR,"e2p4c10")]'''

    def test_string(self):
        a = lexer.Lexer('"string _ 34 */' ' " check')
        b = str(a.extrae_tokens())
        assert b == '''[Token(0,TokenType.STRING,""string _ 34 */ ""), Token(0,TokenType.IDENTIFICADOR,"check")]'''
        c = lexer.Lexer(' "" " " ')
        d = str(c.extrae_tokens())
        assert d == '''[Token(0,TokenType.STRING,""""), Token(0,TokenType.STRING,"" "")]'''

    def test_NUMBER(self):
        a = lexer.Lexer(' 2 2345 2.356 2. ')
        b = str(a.extrae_tokens())
        assert b == '''[Token(0,TokenType.NUMBER,"2"), Token(0,TokenType.NUMBER,"2345"), Token(0,TokenType.NUMBER,"2.356")]'''

    def test_id(self):
        a = lexer.Lexer(' true false and adn burrito')
        b = str(a.extrae_tokens())
        assert b == '''[Token(0,TokenType.TRUE,"true"), Token(0,TokenType.FALSE,"false"), Token(0,TokenType.AND,"and"), Token(0,TokenType.IDENTIFICADOR,"adn"), Token(0,TokenType.IDENTIFICADOR,"burrito")]'''

    def test_total(self):
        a = lexer.Lexer('''class Brunch < Breakfast {
           init(meat, bread, drink) {
               super.init(meat, bread);
               this.drink = drink;
               }
           }''')
        b = str(a.extrae_tokens())
        assert b == '''[Token(0,TokenType.CLASS,"class"), Token(0,TokenType.IDENTIFICADOR,"Brunch"), Token(0,TokenType.LESS,"<"), Token(0,TokenType.IDENTIFICADOR,"Breakfast"), Token(1,TokenType.LEFT_BRACE,"{"), Token(1,TokenType.IDENTIFICADOR,"init"), Token(1,TokenType.LEFT_PAREN,"("), Token(1,TokenType.IDENTIFICADOR,"meat"), Token(1,TokenType.COMMA,","), Token(1,TokenType.IDENTIFICADOR,"bread"), Token(1,TokenType.COMMA,","), Token(1,TokenType.IDENTIFICADOR,"drink"), Token(1,TokenType.RIGHT_PAREN,")"), Token(2,TokenType.LEFT_BRACE,"{"), Token(2,TokenType.SUPER,"super"), Token(2,TokenType.DOT,"."), Token(2,TokenType.IDENTIFICADOR,"init"), Token(2,TokenType.LEFT_PAREN,"("), Token(2,TokenType.IDENTIFICADOR,"meat"), Token(2,TokenType.COMMA,","), Token(2,TokenType.IDENTIFICADOR,"bread"), Token(2,TokenType.RIGHT_PAREN,")"), Token(3,TokenType.SEMICOLON,";"), Token(3,TokenType.THIS,"this"), Token(3,TokenType.DOT,"."), Token(3,TokenType.IDENTIFICADOR,"drink"), Token(3,TokenType.EQUAL,"="), Token(3,TokenType.IDENTIFICADOR,"drink"), Token(4,TokenType.SEMICOLON,";"), Token(5,TokenType.RIGHT_BRACE,"}"), Token(5,TokenType.RIGHT_BRACE,"}")]'''

if __name__ == '__main__':
    unittest.main()
