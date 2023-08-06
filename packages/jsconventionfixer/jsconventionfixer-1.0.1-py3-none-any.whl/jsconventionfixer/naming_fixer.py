import logging
import ntpath
import os
import platform
import re
import string

from jsconventionfixer.lexema import LexemType
from jsconventionfixer.lexer import Lexer
from jsconventionfixer.parser import Parser


class NamingFixer:

    @classmethod
    def verify_project(cls, projpath):
        files_to_verify = []
        for root, dirs, files in os.walk(projpath):
            for f in files:
                if f.endswith(".js"):
                    files_to_verify.append(os.path.join(root, f))
        for f in files_to_verify:
            cls.verify_file(f)

    @classmethod
    def verify_directory(cls, dirpath):
        files = []
        for f in os.listdir(dirpath):
            if f.endswith(".js"):
                files.append(os.path.join(dirpath, f))
        for f in files:
            cls.verify_file(f)

    @classmethod
    def verify_file(cls, filepath):
        fhandler = logging.FileHandler(filename=filepath + '_verification.log', mode='w')
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        fhandler.setFormatter(formatter)

        log = logging.getLogger()  # root logger
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        log.addHandler(fhandler)

        f = open(filepath, 'r')
        text = f.read()
        f.close()
        lexems = Lexer.lex(text)
        Parser.parse(lexems)

        fixes = cls.analyze(lexems)

        for fix in fixes:
            for lexema in lexems:
                if lexema.get_str() == fix[0]:
                    logging.warning(f'{filepath}: {fix[0]} naming error -> should be {fix[1]}')

    @classmethod
    def fix_project(cls, projpath):
        files_to_fix = []
        for root, dirs, files in os.walk(projpath):
            for f in files:
                if f.endswith(".js"):
                    files_to_fix.append(os.path.join(root, f))
        for f in files_to_fix:
            cls.fix_file(f)

    @classmethod
    def fix_directory(cls, dirpath):
        files_to_fix = []
        for f in os.listdir(dirpath):
            if f.endswith(".js"):
                files_to_fix.append(os.path.join(dirpath, f))
        for f in files_to_fix:
            cls.fix_file(f)

    @classmethod
    def fix_file(cls, filepath):
        fhandler = logging.FileHandler(filename=filepath + '_fixing.log', mode='w')
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        fhandler.setFormatter(formatter)

        log = logging.getLogger()  # root logger
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        log.addHandler(fhandler)

        filename = ntpath.basename(filepath)
        dir_path = os.path.dirname(os.path.realpath(filepath))
        clear_filename = filename[0:(len(filename)-3)]
        if not cls.__is_correct_filename(clear_filename):
            new_name = cls.__to_correct_filename(clear_filename)
            slash = "\\" if platform.system() in ['Windows', 'windows', 'Win', 'win'] else "/"
            filepath = dir_path + slash + new_name + ".js"
            os.rename(dir_path + slash + filename, filepath)
            logging.error(f'{filepath}: {filename} naming error -> fixed to {new_name+".js"}')

        f = open(filepath, 'r')
        text = f.read()
        f.close()
        lexems = Lexer.lex(text)
        Parser.parse(lexems)

        fixes = cls.analyze(lexems)

        for fix in fixes:
            for lexema in lexems:
                if lexema.get_str() == fix[0]:
                    lexema.set_str(fix[1])
                    logging.error(f'{filepath}: {fix[0]} naming error -> fixed to {fix[1]}')

        f = open(filepath, 'w')
        for lexema in lexems:
            f.write(lexema.get_str())
        f.close()

    @classmethod
    def analyze(cls, lexems):
        fixes = []
        for lexema in lexems:
            if lexema.get_type() == LexemType.FUNCTION_IDENTIFIER and not cls.__is_camel_case(lexema.get_str()):
                fixes.append((lexema.get_str(), cls.__to_camel_case(lexema.get_str())))
            elif lexema.get_type() == LexemType.PRIVATE_FUNCTION_IDENTIFIER and not cls.__is_trailing_camel_case(lexema.get_str()):
                fixes.append((lexema.get_str(), cls.__to_trailing_camel_case(lexema.get_str())))
            elif lexema.get_type() == LexemType.VARIABLE_IDENTIFIER and not cls.__is_camel_case(lexema.get_str()):
                fixes.append((lexema.get_str(), cls.__to_camel_case(lexema.get_str())))
            elif lexema.get_type() == LexemType.CLASS_IDENTIFIER and not cls.__is_pascal_case(lexema.get_str()):
                fixes.append((lexema.get_str(), cls.__to_pascal_case(lexema.get_str())))
            elif lexema.get_type() == LexemType.CONSTANT_IDENTIFIER and not lexema.get_str().isupper():
                fixes.append((lexema.get_str(), cls.__to_snake(lexema.get_str())))
            elif lexema.get_type() == LexemType.ENUM_IDENTIFIER and not cls.__is_pascal_case(lexema.get_str()):
                fixes.append((lexema.get_str(), cls.__to_pascal_case(lexema.get_str())))
        return fixes

    @classmethod
    def __to_pascal_case(cls, name):
        return string.capwords(name.replace("_", " ")).replace(" ", "")

    @classmethod
    def __to_camel_case(cls, name):
        res = string.capwords(name.replace("_", " ")).replace(" ", "")
        return res[0].lower() + res[1:]

    @classmethod
    def __is_camel_case(cls, name):
        if name[0].isupper():
            return False
        return "_" not in name

    @classmethod
    def __to_trailing_camel_case(cls, name):
        res = string.capwords(name.replace("_", " ")).replace(" ", "")
        res = res[0].lower() + res[1:]
        if res[len(res) - 1] != '_':
            res = res + "_"
        return res

    @classmethod
    def __is_trailing_camel_case(cls, name):
        if name[0].isupper():
            return False
        if name[len(name)-1] != '_':
            return False
        return "_" not in name[0:len(name)-2]

    @classmethod
    def __is_pascal_case(cls, name):
        if name[0].islower():
            return False
        return "_" not in name

    @classmethod
    def __to_snake(cls, name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).upper()

    @classmethod
    def __is_correct_filename(cls, name):
        contains_dashes = "-" in name
        contains_underscores = "_" in name
        contains_uppercase = False
        for ch in name:
            if ch.isupper():
                contains_uppercase = True
                break
        if contains_uppercase:
            return False
        if contains_underscores and contains_dashes:
            return False
        return True

    @classmethod
    def __to_correct_filename(cls, name):
        contains_dashes = "-" in name
        contains_underscores = "_" in name
        if contains_underscores and contains_dashes:
            name = cls.__to_snake(name)
            name = name.lower()
            name = name.replace("_", "-")
        return name
