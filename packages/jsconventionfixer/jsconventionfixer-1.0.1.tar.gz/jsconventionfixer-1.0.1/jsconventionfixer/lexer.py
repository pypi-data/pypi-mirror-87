from jsconventionfixer.lexema import Lexema
from jsconventionfixer.lexema import LexemType
import re

class Lexer:
    @classmethod
    def lex(cls, text):
        str = text
        lexems = []

        while str:
            multi_comment, str = cls.__lex_multi_comment(str)
            if multi_comment:
                lexems.append(multi_comment)
                continue
            comment, str = cls.__lex_comment(str)
            if comment:
                lexems.append(comment)
                continue
            string, str = cls.__lex_str(str)
            if string:
                lexems.append(string)
                continue
            identifier, str = cls.__lex_identifier(str)
            if identifier:
                lexems.append(identifier)
                continue
            number, str = cls.__lex_number(str)
            if number:
                lexems.append(number)
                continue
            whitespace, str = cls.__lex_whitespace(str)
            if whitespace:
                lexems.append(whitespace)
                continue
            symbol, str = cls.__lex_symbol(str)
            if symbol:
                lexems.append(symbol)
                continue
            lexems.append(Lexema(LexemType.UNEXPECTED, str[0]))
            str = str[1:]

        return lexems

    @classmethod
    def __lex_symbol(cls, str):
        if str[0] == '[':
            return Lexema(LexemType.LEFT_BRACKET, str[0:1]), str[1:]
        elif str[0] == ']':
            return Lexema(LexemType.RIGHT_BRACKET, str[0:1]), str[1:]
        elif str[0] == '(':
            return Lexema(LexemType.LEFT_PAREN, str[0:1]), str[1:]
        elif str[0] == ')':
            return Lexema(LexemType.RIGHT_PAREN, str[0:1]), str[1:]
        elif str[0] == '{':
            return Lexema(LexemType.LEFT_BRACE, str[0:1]), str[1:]
        elif str[0] == '}':
            return Lexema(LexemType.RIGHT_BRACE, str[0:1]), str[1:]
        elif str[0] == '<':
            return Lexema(LexemType.LESS_THAN, str[0:1]), str[1:]
        elif str[0] == '>':
            return Lexema(LexemType.GREATER_THAN, str[0:1]), str[1:]
        elif str[0] == '=':
            return Lexema(LexemType.EQUAL, str[0:1]), str[1:]
        elif str[0] == '*':
            return Lexema(LexemType.OPERATOR, str[0:1]), str[1:]
        elif str[0] == '+':
            return Lexema(LexemType.OPERATOR, str[0:1]), str[1:]
        elif str[0] == '%':
            return Lexema(LexemType.OPERATOR, str[0:1]), str[1:]
        elif str[0] == '-':
            return Lexema(LexemType.OPERATOR, str[0:1]), str[1:]
        elif str[0] == '/':
            return Lexema(LexemType.OPERATOR, str[0:1]), str[1:]
        elif str[0] == '&':
            return Lexema(LexemType.OPERATOR, str[0:1]), str[1:]
        elif str[0] == '|':
            return Lexema(LexemType.OPERATOR, str[0:1]), str[1:]
        elif str[0] == '#':
            return Lexema(LexemType.HASH, str[0:1]), str[1:]
        elif str[0] == '.':
            return Lexema(LexemType.DOT, str[0:1]), str[1:]
        elif str[0] == ',':
            return Lexema(LexemType.COMMA, str[0:1]), str[1:]
        elif str[0] == ':':
            return Lexema(LexemType.COLON, str[0:1]), str[1:]
        elif str[0] == ';':
            return Lexema(LexemType.SEMICOLON, str[0:1]), str[1:]
        elif str[0] == '@':
            return Lexema(LexemType.AT, str[0:1]), str[1:]
        elif str[0] == '?':
            return Lexema(LexemType.SEMICOLON, str[0:1]), str[1:]
        elif str[0] == '!':
            return Lexema(LexemType.AT, str[0:1]), str[1:]
        else:
            return None, str

    @classmethod
    def __lex_whitespace(cls, str):
        i = 0
        while i < len(str) and str[i] in ' \n\r\t\v\0\f':
            i += 1

        if i == 0:
            return None, str
        else:
            return Lexema(LexemType.WHITESPACE, str[0:i]), str[i:]

    @classmethod
    def __lex_multi_comment(cls, str):
        if not (str[0] == '/' and str[1] == '*'):
            return None, str
        i = 2

        while i < len(str) - 1 and not (str[i] == '*' and str[i + 1] == '/'):
            i += 1
        if i == len(str) - 1:
            return None, str
        i += 2

        return Lexema(LexemType.MULTI_COMMENT, str[0:i]), str[i:]

    @classmethod
    def __lex_comment(cls, str):
        if not (str[0] == '/' and str[1] == '/'):
            return None, str
        i = 2

        while i < len(str) and str[i] != '\n':
            i += 1

        return Lexema(LexemType.COMMENT, str[0:i]), str[i:]

    @classmethod
    def __lex_identifier(cls, str):
        i = 0
        if str[i] != '_' and not str[i].isalpha():
            return None, str

        while i < len(str) and (str[i].isalpha() or str[i].isnumeric() or str[i] == '_'):
            i += 1

        return Lexema(LexemType.IDENTIFIER, str[0:i]), str[i:]

    @classmethod
    def __lex_str(cls, str):
        if str[0] != '\'' and str[0] != '\"':
            return None, str

        quote = str[0]
        i = 1

        while str[i] != quote:
            i += 1
        i += 1

        return Lexema(LexemType.STRING, str[0:i]), str[i:]

    @classmethod
    def __lex_number(cls, str):
        numbers = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", str)
        if len(numbers) == 0:
            return None, str

        first_number = numbers[0]
        number_len = len(first_number)

        p_number = str[0:number_len]
        if p_number == first_number:
            return Lexema(LexemType.NUMBER, first_number), str[number_len:]
        else:
            return None, str
