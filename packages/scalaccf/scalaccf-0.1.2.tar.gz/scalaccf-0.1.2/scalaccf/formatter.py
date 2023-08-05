from scalaccf.lexer import TokenType, Token


class Formatter:
    class_keywords = ['class', 'trait', 'object']

    def __init__(self, tokens):
        self.__tokens = tokens

    @staticmethod
    def snake_to_lower_camel_case(naming):
        if naming.isupper():
            naming = naming.lower()
        if naming.find('_') != -1 and naming[0].isupper():
            return naming[0].lower() + naming[1:]
        components = naming.split('_')
        return components[0] + ''.join(x[0].capitalize() + x[1:] for x in components[1:])

    @staticmethod
    def __is_not_lower_camel_case(naming):
        if naming == '_':
            return False
        return naming.find('_') != -1 or naming[0].isupper()

    @staticmethod
    def __is_not_upper_camel_case(naming):
        if naming == '_':
            return False
        return naming.find('_') != -1 or naming[0].islower()

    @staticmethod
    def __is_lower_case(naming):
        return naming[0].islower()

    @staticmethod
    def snake_to_upper_camel_case(naming):
        return Formatter.snake_to_lower_camel_case(naming).title()

    def format(self):
        self.__fix_comments()
        self.__fix_namings()
        self.__fix_type_params()
        return self.__tokens

    def fix_filename(self, filename):
        # upper case camel case for files with single logical compilation unit
        # lower case camel case for multi-unit files
        if self.__count_classes() > 1 and Formatter.__is_not_upper_camel_case(filename):
            return Formatter.snake_to_upper_camel_case(filename)
        elif Formatter.__is_not_lower_camel_case(filename):
            return Formatter.snake_to_lower_camel_case(filename)
        return None

    def __count_classes(self):
        i = 0
        count = 0
        class_names = []
        while i < len(self.__tokens):
            if self.__tokens[i].get_value() in Formatter.class_keywords:
                i = self.__skip_ws_tokens(i + 1)
                if self.__tokens[i].get_value() not in class_names:
                    class_names.append(self.__tokens.get_value())
                    count += 1
                i += 1
        return count

    def __fix_namings(self):
        stack = []
        i = 0
        while i < len(self.__tokens):
            token = self.__tokens[i]
            # upper case camel case for object types
            if token.get_value() == ':':
                i = self.__skip_ws_tokens(i + 1)
                if self.__tokens[i].get_token_type() == TokenType.IDENTIFIER:
                    if Formatter.__is_not_upper_camel_case(self.__tokens[i].get_value()):
                        self.__tokens[i].set_fixed_value(
                            Formatter.snake_to_upper_camel_case(self.__tokens[i].get_value()))
                    i += 1
            # lower case camel case for annotation
            elif token.get_token_type() == TokenType.ANNOTATION and Formatter.__is_not_lower_camel_case(
                    token.get_value()):
                token.set_fixed_value(Formatter.snake_to_lower_camel_case(token.get_value()))
                i += 1
            # package as in Java naming convention
            elif token.get_value() == 'package':
                i = self.__fix_packages(i) - 1
            # upper case camel case for class, trait & object
            elif token.get_value() == 'extends':
                i = self.__fix_class_trait_object(i) - 1
            elif token.get_value() in Formatter.class_keywords:
                if token.get_value() == 'object' and self.__tokens[i - 2].get_value() == 'package':
                    i = self.__fix_packages(i) - 1
                    continue
                stack.append(token.get_value())
                i = self.__fix_class_trait_object(i) - 1
            elif token.get_token_type() == TokenType.IDENTIFIER and token.get_fixed_value() is None and \
                    Formatter.__is_not_lower_camel_case(token.get_value()):
                token.set_fixed_value(Formatter.snake_to_lower_camel_case(token.get_value()))
                i += 1
            else:
                i += 1

    def __fix_type_params(self):
        brace_count = 0
        for token in self.__tokens:
            if token.get_value() == '[':
                brace_count += 1
            elif token.get_value() == ']':
                brace_count -= 1
            elif brace_count > 0 and token.get_token_type() == TokenType.IDENTIFIER and Formatter.__is_not_upper_camel_case(
                    token.get_value()):
                token.set_fixed_value(Formatter.snake_to_upper_camel_case(token.get_value()))

    def __fix_packages(self, pos):
        pos = self.__skip_ws_tokens(pos + 1)
        while self.__tokens[pos].get_value() != '\n':
            token = self.__tokens[pos]
            if token.get_token_type() == TokenType.IDENTIFIER and Formatter.__is_not_lower_camel_case(
                    token.get_value()):
                token.set_fixed_value(Formatter.snake_to_lower_camel_case(token.get_value()))
            pos += 1
        return pos

    def __fix_class_trait_object(self, pos):
        pos = self.__skip_ws_tokens(pos + 1)
        if self.__tokens[pos].get_token_type() == TokenType.IDENTIFIER and Formatter.__is_not_upper_camel_case(
                self.__tokens[pos].get_value()):
            fixed_value = Formatter.snake_to_upper_camel_case(self.__tokens[pos].get_value())
            self.__tokens[pos].set_fixed_value(fixed_value)
            pos += 1
        return pos

    def __fix_comments(self):
        # Fix documentation comments
        i = 0
        while i < len(self.__tokens):
            token = self.__tokens[i]
            if token.get_token_type() == TokenType.COMMENT \
                    and token.get_value().startswith('/**'):
                token.set_fixed_value(Formatter.__fix_links(self.__tokens[i].get_value()))
            elif token.get_value() in ('def', 'package', 'class', 'trait', 'object'):
                pos = self.__find_comment_before(i)
                comment = None
                if pos != -1:
                    comment = self.__tokens[pos]
                if token.get_value() == 'def':
                    self.__fix_method_comment(i, comment)
                elif token.get_value() == 'package':
                    self.__fix_package_comment(i, comment)
                elif token.get_value() == 'class':
                    self.__fix_class_comment(i, comment)
                elif token.get_value() == 'trait':
                    self.__fix_trait_comment(i, comment)
                elif token.get_value() == 'object':
                    self.__fix_object_comment(i, comment)
                i += 1
            i += 1

    def __find_comment_before(self, pos):
        while self.__tokens[pos].get_value() != '\n' \
                and pos >= 0:
            pos -= 1
            if self.__tokens[pos].get_token_type() == TokenType.COMMENT and self.__tokens[
                pos].get_value().startswith('/**'):
                return pos
        pos = self.__skip_throws_before(pos)
        if self.__tokens[pos - 1].get_token_type() == TokenType.COMMENT and self.__tokens[
            pos - 1].get_value().startswith('/**'):
            return pos - 1
        return -1

    def __skip_throws_before(self, pos):
        last_throws = pos
        while pos > 0:
            if self.__tokens[pos] == '\n':
                token_before = pos
                while self.__tokens[token_before].get_token_type() == TokenType.COMMENT and token_before >= 0:
                    token_before -= 1
                token_after = self.__skip_ws_tokens(pos + 1)
                is_valid_next_token = self.__tokens[token_after].get_value() == 'throws' \
                                      or self.__tokens[token_after].get_value() in Formatter.class_keywords \
                                      or self.__tokens[token_after].get_value() == 'def'
                if self.__tokens[token_before].get_token_type() == TokenType.COMMENT \
                        and is_valid_next_token:
                    last_throws = token_before
                elif not is_valid_next_token:
                    return last_throws
            pos -= 1
        return last_throws

    def __fix_package_comment(self, pos, comment=None):
        if comment is not None:
            return
        ws = ''
        i = pos - 1
        while self.__tokens[i].get_value() != '\n' and i > 0:
            i -= 1
        pos = i
        i += 1
        while self.__tokens[i].get_token_type() == TokenType.WHITESPACE:
            ws += ' '
            i += 1
        classes = self.__find_classes_under_package(pos)
        if len(classes) == 0:
            return
        comment = ws + '/** '
        package = self.find_package()
        if Formatter.__is_not_lower_camel_case(package) and Formatter.__is_not_lower_camel_case(package):
            package = Formatter.snake_to_lower_camel_case(package)
        components = package.split('.')
        package = '.'.join(
            Formatter.snake_to_lower_camel_case(component) if Formatter.__is_not_lower_camel_case(
                component) else comment for
            component in components)
        for i in classes:
            comment += f'Class implemented in this package is [[{package}.{self.snake_to_upper_camel_case(i) if Formatter.__is_not_upper_camel_case(i) else i}]]\n'
        comment += ws + '*/\n' + ws

        token = Token(None, TokenType.COMMENT, self.__tokens[pos].get_position())
        token.set_fixed_value(comment)
        self.__tokens.insert(pos, token)

    def __find_classes_under_package(self, pos):
        bracket_found = False
        bracket_count = 0
        classes = []
        while bracket_count != 0 and not bracket_found:
            if self.__tokens[pos].get_value() != '\n' and not bracket_found:
                return None
            elif self.__tokens[pos].get_value() == '{':
                bracket_found = True
                bracket_count += 1
            elif self.__tokens[pos].get_value() == '}':
                bracket_count -= 1
            elif self.__tokens[pos].get_value() == 'class':
                pos = self.__skip_ws_tokens(pos)
                classes.append(self.__tokens[pos])
            pos += 1
        return classes

    def find_package(self):
        i = 0
        package_found = False
        package = list()
        while i < len(self.__tokens):
            token = self.__tokens[i]
            if token.get_value() == 'package':
                package_found = True
            elif token.get_value() in ('class', 'trait', 'object', 'import'):
                return package
            elif package_found and \
                    token.get_token_type() == TokenType.IDENTIFIER:
                package.append(token.get_value())
            elif token.get_value() == '{':
                return package[:-1]
            i += 1
        return package

    def __fix_trait_comment(self, pos, comment=None):
        if comment is not None:
            return
        ws = ''
        i = pos - 1
        while self.__tokens[i].get_value() != '\n' and i > 0:
            i -= 1
        pos = i
        i += 1
        while self.__tokens[i].get_token_type() == TokenType.WHITESPACE:
            ws += ' '
            i += 1
        pos = i
        params = self.__find_trait_params(pos)
        comment = '\n' + ws + '/** '
        for i in params:
            comment += f'{Formatter.snake_to_lower_camel_case(i) if Formatter.__is_not_lower_camel_case(i) else i} must be specified in class using this\n'
        comment += ws + '*/\n' + ws
        token = Token(None, TokenType.COMMENT, self.__tokens[pos].get_position())
        token.set_fixed_value(comment)
        self.__tokens.insert(pos, token)

    def __find_trait_params(self, pos):
        bracket_found = False
        bracket_count = 0
        parameters = []
        while bracket_count != 0 and not bracket_found:
            if self.__tokens[pos].get_value() != '\n' and not bracket_found:
                return None
            elif self.__tokens[pos].get_value() == '{':
                bracket_found = True
                bracket_count += 1
            elif self.__tokens[pos].get_value() == '}':
                bracket_count -= 1
            elif self.__tokens[pos].get_value() == 'def':
                pos = self.__skip_ws_tokens(pos)
                if not self.__is_equals_in_line(pos):
                    parameters.append(self.__tokens[pos].get_value())
            pos += 1
        return parameters

    def __is_equals_in_line(self, pos):
        while self.__tokens[pos].get_value() != '\n':
            pos += 1
            if self.__tokens[pos].get_value() == '=':
                return True
        return False

    def __fix_class_comment(self, pos, comment=None):
        name = self.__find_class_name(pos)
        type_params = self.__find_type_params(pos)
        params = self.__find_params(pos)
        throws = self.__find_throws(pos)
        extends = self.__find_extends(pos)

        if comment is not None:
            comment.set_fixed_value(Formatter.__replace_in_comment('@tparam', type_params, comment.get_value(), True))
            comment.set_fixed_value(Formatter.__replace_in_comment('@param', params, comment.get_value(), False))
            comment.set_fixed_value(Formatter.__replace_in_comment('@throws', throws, comment.get_value(), True))
            comment.set_fixed_value(Formatter.__replace_in_comment('@extends', extends, comment.get_value(), True))

            comment.set_fixed_value(
                Formatter.__add_to_comment_if_not_exists('@tparam', type_params, comment.get_value(), True))
            comment.set_fixed_value(
                Formatter.__add_to_comment_if_not_exists('@param', params, comment.get_value(), False))
            comment.set_fixed_value(
                Formatter.__add_to_comment_if_not_exists('@throws', throws, comment.get_value(), True))
            comment.set_fixed_value(
                Formatter.__add_to_comment_if_not_exists('@extends', extends, comment.get_value(), True))
        else:
            ws = ''
            i = pos - 1
            while self.__tokens[i].get_value() != '\n' and i > 0:
                i -= 1
            pos = i
            i += 1
            while self.__tokens[i].get_token_type() == TokenType.WHITESPACE:
                ws += ' '
                i += 1
            type_params = [
                self.snake_to_upper_camel_case(param) if Formatter.__is_not_upper_camel_case(param) else param for
                param in type_params]
            params = [
                Formatter.snake_to_lower_camel_case(param) if Formatter.__is_not_lower_camel_case(param) else param
                for param in params]
            throws = [self.snake_to_upper_camel_case(throw) if Formatter.__is_not_upper_camel_case(throw) else throw
                      for throw in throws]
            extends = [self.snake_to_upper_camel_case(value) if Formatter.__is_not_upper_camel_case(value) else value
                       for value in extends]

            comment = '\n' + ws + '/** '
            comment += f"@constructor Create a new {name}{' with specified ' if len(params) > 0 else ''}{', '.join(params)}\n"
            for i in type_params:
                comment += ws + f'  * @tparam {i}\n'
            for i in params:
                comment += ws + f'  * @param {i}\n'
            for i in throws:
                comment += ws + f'  * @throws {i}\n'
            for i in extends:
                comment += ws + f'  * @extends {i}\n'
            comment += ws + '*/'
            token = Token(None, TokenType.COMMENT, self.__tokens[pos].get_position())
            token.set_fixed_value(comment)
            self.__tokens.insert(pos, token)

    @staticmethod
    def __replace_in_comment(param, tokens, comment, upper):
        pos = 0
        while pos < len(comment):
            pos = comment.find(param, pos)
            if pos == -1:
                return comment
            token_start = 0
            token_end = 0
            token_found = False
            while pos < len(comment):
                if comment[pos] == '@':
                    while comment[pos] != ' ':
                        pos += 1
                elif token_found and comment[pos] in (' ', '\n'):
                    token_end = pos
                    token_found = False
                    break
                elif comment[pos] not in (' ', '\n') and not token_found:
                    token_found = True
                    token_start = pos
                elif comment[pos] == '\n':
                    pos += 1
                    continue
                pos += 1

            if token_end <= 0:
                token_end = len(comment) - 1

            token = comment[token_start:token_end]
            if token in tokens or Formatter.snake_to_lower_camel_case(
                    token) in tokens or Formatter.snake_to_upper_camel_case(token) in tokens:
                if upper and Formatter.__is_not_upper_camel_case(token):
                    token = Formatter.snake_to_upper_camel_case(token)
                elif not upper and Formatter.__is_not_lower_camel_case(token):
                    token = Formatter.snake_to_lower_camel_case(token)
            comment = comment[:token_start] + token + comment[token_end:]
            pos = token_end + 1
        return comment

    @staticmethod
    def __remove_line(pos, comment):
        start = pos
        end = pos

        while start > 0 and comment[start] != '\n':
            start -= 1
        while end < len(comment) and comment[end] != '\n':
            end += 1

        return comment[:start] + comment[end:]

    def __fix_method_comment(self, pos, comment=None):
        params = self.__find_params(pos)
        throws = self.__find_throws(pos)
        (returns_before, returns) = self.__find_and_format_returns(pos)

        ws = ''
        i = pos - 1
        while self.__tokens[i].get_value() != '\n' and i > 0:
            i -= 1
        pos = i
        i += 1
        while self.__tokens[i].get_token_type() == TokenType.WHITESPACE:
            ws += ' '
            i += 1

        if comment is not None:
            comment.set_fixed_value(Formatter.__replace_in_comment('@param', params, comment.get_value(), False))
            comment.set_fixed_value(Formatter.__replace_in_comment('@throws', throws, comment.get_value(), True))
            comment.set_fixed_value(
                Formatter.__replace_in_comment('@return', returns_before, comment.get_value(), True))
            if len(returns_before) > 0:
                comment.set_fixed_value(
                    Formatter.__replace_in_comment('@return', Formatter.snake_to_lower_camel_case(
                        returns_before[0].lower() + returns_before[1:]),
                                                   comment.get_value(), True))
            comment.set_fixed_value(
                Formatter.__add_to_comment_if_not_exists('@param', params, comment.get_value(), False, ws))
            comment.set_fixed_value(
                Formatter.__add_to_comment_if_not_exists('@throws', throws, comment.get_value(), True, ws))
            if returns != '':
                comment.set_fixed_value(
                    Formatter.__add_to_comment_if_not_exists('@return', [returns], comment.get_value(), True, ws))
        else:
            params = [
                Formatter.snake_to_lower_camel_case(param) if Formatter.__is_not_lower_camel_case(param) else param
                for param in params]
            throws = [self.snake_to_upper_camel_case(throw) if Formatter.__is_not_upper_camel_case(throw) else throw
                      for throw in throws]

            if len(throws) > 0 or len(params) > 0 or returns is not None:
                if len(params) > 0:
                    comment = '\n' + ws + f'/** @param {params[0]}\n'
                    i = 1
                    while i < len(params):
                        comment += ws + f'  * @param {params[i]}\n'
                        i += 1
                    i = 0
                elif len(throws) > 0:
                    comment = '\n' + ws + f'/** @throws {throws[0]}\n'
                    i = 1
                else:
                    comment = '\n' + ws + f'/** @return {returns}\n'
                if len(throws) > 0:
                    while i < len(throws):
                        comment += ws + f'  * @throws {throws[i]}\n'
                        i += 1
                if len(throws) > 0 or len(params) > 0:
                    comment += ws + f'  * @return {returns}\n'
                comment += ws + '*/'
            else:
                comment = '\n' + ws + '/** */'
            token = Token(None, TokenType.COMMENT, self.__tokens[pos].get_position())
            token.set_fixed_value(comment)
            self.__tokens.insert(pos, token)

    def __find_class_name(self, pos):
        while self.__tokens[pos].get_value() != 'class':
            pos += 1
        return self.__tokens[self.__skip_ws_tokens(pos + 1)].get_value()

    def __find_and_format_returns(self, pos):
        brace_found = False
        colon_found = False
        returns_before = ''
        returns = ''
        pos += 1
        while self.__tokens[pos].get_value() not in ('{', '=', 'val', 'def') and \
                self.__tokens[pos].get_value() not in Formatter.class_keywords:
            token = self.__tokens[pos]
            if token.get_value() == ')':
                brace_found = True
            elif brace_found and token.get_value() == ':':
                colon_found = True
            elif colon_found and token.get_token_type() == TokenType.IDENTIFIER or token.get_value() == (',', '[', ']'):
                returns_before += token.get_value()
                returns += self.snake_to_upper_camel_case(token.get_value()) if Formatter.__is_not_upper_camel_case(
                    token.get_value()) else token.get_value()
            pos += 1
        return returns_before, returns

    def __find_params(self, pos):
        params = []
        brace_found = False
        colon_found = False
        while self.__tokens[pos].get_value() not in ('{', '='):
            token = self.__tokens[pos]
            if token.get_value() == '(':
                brace_found = True
            elif token.get_value() == ')' and brace_found:
                return params
            elif token.get_value() == ':':
                colon_found = True
            elif token.get_value() == ',' and colon_found:
                colon_found = False
            elif token.get_token_type() == TokenType.IDENTIFIER \
                    and brace_found and not colon_found:
                params.append(token.get_value())
            pos += 1
        return params

    def __find_type_params(self, pos):
        type_params = []
        square_bracket_found = False
        while self.__tokens[pos].get_value() not in ('{', '=', '('):
            token = self.__tokens[pos]
            if token.get_value() == '[':
                square_bracket_found = True
            elif token.get_value() == ']':
                return type_params
            elif square_bracket_found and token.get_token_type() == TokenType.IDENTIFIER:
                type_params.append(token.get_value())
            pos += 1
        return type_params

    def __find_throws(self, pos):
        throws = []
        while self.__tokens[pos].get_value() not in ('{', '='):
            if self.__tokens[pos].get_value() == '@throws' \
                    and self.__tokens[pos + 1].get_value() == '[':
                throws.append(self.__tokens[pos + 2].get_value())
            pos += 1
        return throws

    def __fix_object_comment(self, pos, comment=None):
        extends = self.__find_extends(pos)
        if comment is not None:
            comment.set_fixed_value(Formatter.__replace_in_comment('@extends', extends, comment.get_value(), True))

            comment.set_fixed_value(
                Formatter.__add_to_comment_if_not_exists('@extends', extends, comment.get_value(), True))
        else:
            comment = '\n' + '/** '
            for i in extends:
                comment += f'@extends {i}\n'
            comment += '*/\n'
            token = Token(None, TokenType.COMMENT, self.__tokens[pos].get_position())
            token.set_fixed_value(comment)
            self.__tokens.insert(pos, token)

    def __find_extends(self, pos):
        extends = []
        extends_found = False
        pos += 1
        while self.__tokens[pos].get_value() not in ('{', '=', 'def') and self.__tokens[
            pos].get_value() not in Formatter.class_keywords:
            if self.__tokens[pos].get_value() == 'extends':
                extends_found = True
            elif extends_found and self.__tokens[pos].get_token_type() == TokenType.IDENTIFIER:
                extends.append(self.__tokens[pos].get_value())
            else:
                pass
            pos += 1
        return extends

    @staticmethod
    def __fix_links(comment):
        i = 0
        while i < len(comment):
            if comment[i] == '[' and comment[i + 1] == '[':
                link_start = i + 1
                link_end = comment.find(i + 1, ']')
                link = comment[link_start + 1:link_end]
                comment = comment[:link_start] + Formatter.__fix_link(link) + comment[link_end:]
                i = link_end
            i += 1
        return comment

    @staticmethod
    def __fix_link(link):
        components = link.split('.')
        components = [Formatter.snake_to_lower_camel_case(component) if Formatter.__is_not_lower_camel_case(
            component) else component for component in components]
        components[-1] = components[-1].title()
        return '.'.join(components)

    def __skip_ws_tokens(self, pos):
        while pos < len(self.__tokens):
            if self.__tokens[pos].get_token_type() != TokenType.WHITESPACE:
                return pos
            pos += 1

    @staticmethod
    def __add_to_comment_if_not_exists(param, tokens, comment, upper, ws=''):
        pos = 0
        params = Formatter.__get_params_in_comment(param, comment)
        for token in tokens:
            if token in ('', ' ', '\n') or token is None or len(token) == 0:
                pass
            if token not in params and Formatter.snake_to_upper_camel_case(
                    token) not in params and Formatter.snake_to_lower_camel_case(token) not in params:
                pos = Formatter.__find_end_of_params(param, comment)
                token = Formatter.snake_to_upper_camel_case(token) if upper and Formatter.__is_not_upper_camel_case(
                    token) else token
                token = Formatter.snake_to_lower_camel_case(token) if not upper and Formatter.__is_not_lower_camel_case(
                    token) else token
                comment = comment[:pos] + '\n' + ws + f'  * {param} {token}' + comment[pos:]

        return comment

    @staticmethod
    def __get_params_in_comment(param, comment):
        pos = 0
        tokens = []
        while pos < len(comment):
            pos = comment.find(param, pos)
            if pos == -1:
                return tokens
            token_start = 0
            token_end = 0
            token_found = False
            while pos < len(comment):
                if comment[pos] == '@':
                    while comment[pos] != ' ':
                        pos += 1
                elif token_found and comment[pos] in (' ', '\n'):
                    token_end = pos
                    token_found = False
                    break
                elif comment[pos] not in (' ', '\n') and not token_found:
                    token_found = True
                    token_start = pos
                elif comment[pos] == '\n':
                    pos += 1
                    continue
                pos += 1
            if token_end <= 0:
                token_end = len(comment) - 1
            token = comment[token_start:token_end]
            if token != '*':
                tokens.append(token)
            pos += 1
        return tokens

    @staticmethod
    def __find_end_of_params(param, comment):
        last_occurrence = comment.rfind(param)
        if last_occurrence == -1:
            i = len(comment) - 1
            star_count = 0
            while i >= 0:
                if comment[i] == '*':
                    star_count += 1
                    if star_count == 2:
                        return i + 1
                elif comment[i] not in (' ', '\n'):
                    star_count = 0
                elif comment[i] == '\n' and star_count == 1:
                    return i
        else:
            i = last_occurrence
            while comment[i] not in ('\n', '*'):
                i += 1
            return i
