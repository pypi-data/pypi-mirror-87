import logging
import os
from scalaccf.lexer import Lexer, TokenType
from scalaccf.formatter import Formatter


class CCF:
    def __init__(self, files):
        self.__files = files

    def verify(self):
        if not os.path.exists('verification'):
            os.mkdir('verification')
        tokens_list = []
        for file in self.__files:
            tokens_list.append(Lexer(file).get_tokens())
        i = 0
        namings = dict()
        while i < len(tokens_list):
            tokens = tokens_list[i]
            file = self.__files[i]
            logging.basicConfig(filename=os.path.join('verification', f'{file.split(".")[0]}_verification.log'),
                                level=logging.WARN)
            formatter = Formatter(tokens)
            expected_file_name = formatter.fix_filename(file)
            if expected_file_name is not None and expected_file_name != file:
                logging.warning(
                    f'{file}: Wrong file naming: Expected {expected_file_name}, but found {file}')
            namings.update(formatter.find_namings_to_fix())
            tokens_list[i] = formatter.get_tokens()
            i += 1
        i = 0
        while i < len(tokens_list):
            tokens = tokens_list[i]
            file = self.__files[i]
            formatter = Formatter(tokens)
            formatter.fix_namings(namings)
            for token in tokens:
                if token.get_fixed_value() is not None and token.get_primary_value() != token.get_fixed_value():
                    logging.warning(f'{file}: [{token.get_position()[0]}, {token.get_position()[1]}] - '
                                    f'Error Code: {CCF.get_error_description(token)}\n'
                                    f'Expected {token.get_fixed_value()}, but found {token.get_primary_value()}\n\n')
            i += 1

    def fix(self):
        if not os.path.exists('fixing'):
            os.mkdir('fixing')
        tokens_list = []
        for file in self.__files:
            tokens_list.append(Lexer(file).get_tokens())
        i = 0
        namings = dict()
        while i < len(tokens_list):
            tokens = tokens_list[i]
            file = self.__files[i]
            logging.basicConfig(filename=os.path.join('fixing', f'{file.split(".")[0]}_fixing.log'), level=logging.WARN)
            formatter = Formatter(tokens)
            expected_file_name = formatter.fix_filename(file)
            if expected_file_name is not None and expected_file_name != file:
                logging.warning(f'{file}: Wrong namings in path: Expected {expected_file_name}, but found {file}')
                os.rename(file, expected_file_name)
                file = expected_file_name
            namings.update(formatter.find_namings_to_fix())
            tokens_list[i] = formatter.get_tokens()
            i += 1
        i = 0
        while i < len(tokens_list):
            tokens = tokens_list[i]
            file = self.__files[i]
            formatter = Formatter(tokens)
            formatter.fix_namings(namings)
            for token in tokens:
                if token.get_fixed_value() is not None and token.get_primary_value() != token.get_fixed_value():
                    logging.warning(f'{file}: [{token.get_position()[0]}, {token.get_position()[1]}] - '
                                    f'Modification: Changed {token.get_primary_value()} to {token.get_fixed_value()}\n\n')
            CCF.write_tokens_to_file(file, tokens)
            i += 1

    @staticmethod
    def get_fixed_filename(filename, formatter):
        filename_parts = filename.split('.')
        return formatter.snake_to_upper_camel_case(filename_parts[0]) + '.' + '.'.join(filename_parts[1:])

    @staticmethod
    def get_error_description(token):
        if token.get_token_type() == TokenType.COMMENT:
            return 'Errors in documentation comment'
        elif token.get_token_type() == TokenType.ANNOTATION:
            return 'Wrong style for annotation'
        elif token.get_token_type() == TokenType.IDENTIFIER:
            if token.get_fixed_value()[0].isupper():
                return 'Wrong style for class, trait or object'
            else:
                return 'Wrong style for package, variable or method'

    @staticmethod
    def write_tokens_to_file(filename, tokens):
        file = open(filename, mode='w+')
        for token in tokens:
            file.write(token.get_value())
        file.close()
