from enum import Enum
KEYWORDS = (
    "abstract", "arguments", "await", "boolean",
    "break", "byte", "case", "catch",
    "char", "class", "const",
    "continue", "debugger", "default", "delete",
    "do", "double", "else", "enum",
    "eval", "export", "extends", "false",
    "final", "finally", "float", "for",
    "function", "goto", "if", "implements",
    "import", "int", "in", "instanceof",
    "interface", "let", "long", "native",
    "new", "null", "private", "package",
    "protected", "public",
    "return", "short",
    "static", "super",
    "synchronized", "switch", "this", "throw",
    "true", "try", "typeof", "throws",
    "transient", "var", "with", "yield",
    "void", "volatile",
    "while"
)

class LexemType(Enum):
    NUMBER = 0,
    IDENTIFIER = 1,
    STRING = 2,
    LEFT_BRACKET = 3,
    RIGHT_BRACKET = 4,
    LEFT_PAREN = 5,
    RIGHT_PAREN = 6,
    LEFT_BRACE = 7,
    RIGHT_BRACE = 8,
    LESS_THAN = 9,
    GREATER_THAN = 10,
    EQUAL = 11,
    OPERATOR = 12,
    SLASH = 13,
    HASH = 14,
    DOT = 15,
    COMMA = 16,
    COLON = 17,
    SEMICOLON = 18,
    COMMENT = 19,
    MULTI_COMMENT = 20,
    WHITESPACE = 21,
    UNEXPECTED = 22,
    KEYWORD = 23,
    FUNCTION_IDENTIFIER = 24,
    CLASS_IDENTIFIER = 25,
    VARIABLE_IDENTIFIER = 26,
    AT = 27,
    PRIVATE_FUNCTION_IDENTIFIER = 28,
    CONSTANT_IDENTIFIER = 29,
    ENUM_IDENTIFIER = 30


class Lexema:
    def __init__(self, lexem_type, str, line=-1):
        self.__lexem_type = lexem_type
        self.__str = str
        self.__line = line

    def has_type(self, lexem_type):
        return self.__lexem_type == lexem_type

    def get_str(self):
        return self.__str

    def set_str(self, new_str):
        self.__str = new_str

    def get_line(self):
        return self.__line

    def get_type(self):
        return self.__lexem_type

    def set_type(self, new_type):
        self.__lexem_type = new_type
