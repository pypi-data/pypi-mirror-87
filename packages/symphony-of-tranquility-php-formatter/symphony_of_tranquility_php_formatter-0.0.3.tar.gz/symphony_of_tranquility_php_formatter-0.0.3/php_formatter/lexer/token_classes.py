from .dict_token_types import Tokens


class Token:

    def __init__(self, token_type=None, row=None, column=None,  index=None, spec=None):
        self.type = token_type
        self.spec = spec
        self.index = index
        self.row = row
        self.column = column

    def set_invalid(self):
        self.index = self.row = self.column = self.spec = None
        self.type = Tokens.Invalid

    def is_fake(self):
        return self.type is None and self.spec is None and \
               self.index is None and self.row is None and self.column is None

    def __str__(self):
        ans = ''
        if self.type is not None:
            if self.spec is not None:
                ans += str(self.type).ljust(20)
            else:
                ans += str(self.type).ljust(40)
        if self.spec is not None:
            ans += (' ( ' + self.spec + ' ) ').ljust(20)
        if self.row is not None:
            ans += '|' + (str(self.row)).rjust(2) + '|'
        if self.column is not None:
            ans += (str(self.column)).ljust(2) + ('|').ljust(10)

        return ans


class WrongToken:

    def __init__(self, message=None, token=None, format_type=None, old_value=None, new_value=None):
        self.error_message = message
        self.token = token
        self.format_type = format_type
        self.old_value = old_value
        self.new_value = new_value

    def __str__(self):
        s = str(self.token) + ' | ' + self.error_message.ljust(50)
        if self.format_type is not None:
            s += ' | ' + self.format_type.ljust(12)
        return s
