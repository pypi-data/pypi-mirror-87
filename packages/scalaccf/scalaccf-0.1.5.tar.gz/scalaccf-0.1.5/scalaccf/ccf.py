import logging
import os
from os.path import abspath
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
        for tokens in tokens_list:
            logging.basicConfig(filename=f'verification/{file.split(".")[0]}_verification.log', level=logging.WARN)
            formatter = Formatter(tokens)
            expected_path, found_path = CCF.get_fixed_path(file, formatter)
            if expected_path != found_path:
                logging.warning(
                    f'{found_path}: Wrong file namings in path: Expected {expected_path}, but found {found_path}')
            tokens = formatter.format()
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
        for tokens in tokens_list:
            logging.basicConfig(filename=f'fixing/{file.split(".")[0]}_fixing.log', level=logging.WARN)
            formatter = Formatter(tokens)
            expected_path, found_path = CCF.get_fixed_path(file, formatter)
            if expected_path != found_path:
                logging.warning(f'{file}: Wrong namings in path: Expected {expected_path}, but found {found_path}')
                file = CCF.fix_path(expected_path, found_path, file)
            tokens = formatter.format()
            CCF.__fix_tokens(i, tokens_list)
            for token in tokens:
                if token.get_fixed_value() is not None and token.get_primary_value() != token.get_fixed_value():
                    logging.warning(f'{file}: [{token.get_position()[0]}, {token.get_position()[1]}] - '
                                    f'Modification: Changed {token.get_primary_value()} to {token.get_fixed_value()}\n\n')
            CCF.write_tokens_to_file(file, tokens)
            i += 1

    @staticmethod
    def fix_path(expected_path, found_path, file):
        current_path = ''
        if len(expected_path) != len(found_path) and len(found_path) == 2:
            current_path = CCF.split_path(abspath(file))[:-1]
        else:
            current_path = CCF.split_path(abspath(file))[:-len(found_path)]

        os.chdir(os.path.join(*current_path))
        path = current_path
        path.extend(expected_path[:-1])
        if not os.path.exists(os.path.join(*expected_path[:-1])):
            os.makedirs(os.path.join(*expected_path[:-1]))

        with open(os.path.join(os.path.join(*path), expected_path[-1]), 'w+'):
            pass
        return os.path.join(os.path.join(*path), expected_path[-1])

    @staticmethod
    def get_fixed_path(file, formatter):
        package = formatter.find_package()
        file_path = os.path.abspath(file)
        path = CCF.split_path(file_path)

        if len(package) <= 0 or len(path) <= 1:
            return path, path

        file_name = path[-1]

        expected = CCF.get_fixed_package(package, formatter)
        expected.append(CCF.get_fixed_filename(file_name, formatter))

        found = ''

        if package[-1] != path[-2]:
            found = path[-2:]
        else:
            found = path[len(path) - len(package) - 1:]

        return expected, found

    @staticmethod
    def split_path(file_path):
        path = []
        while 1:
            file_path, folder = os.path.split(file_path)
            if folder != '':
                path.append(folder)
            elif file_path != '':
                path.append(file_path)
                break

        path.reverse()
        return path

    @staticmethod
    def get_fixed_package(package, formatter):
        fixed = []
        for folder in package:
            fixed.append(formatter.snake_to_lower_camel_case(folder))
        return fixed

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

    @staticmethod
    def __fix_tokens(pos, tokens_list):
        tokens = tokens_list[pos]
        i = 0
        while i < len(tokens_list):
            if i != pos:
                other_tokens = tokens_list[i]
                for token in tokens:
                    for other_token in other_tokens:
                        if token.get_primary_value() == other_token.get_primary_value() and \
                                other_token.get_fixed_value() is None:
                            other_token.set_fixed_value(token.get_value())
            i += 1
