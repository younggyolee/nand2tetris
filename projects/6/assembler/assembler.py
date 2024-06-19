# read file
def read_text_file(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

file_name = 'Add.asm'
text = read_text_file(file_name)

# parser
class Parser:
    def __init__(self, text):
        text = text.replace(' ', '') # removes all white spaces
        lines = text.split('\n')
        lines = [x for x in lines if len(x) > 0] # removes empty lines

        # remove comments
        for i, line in enumerate(lines):
            comment_index = line.find('//')
            if comment_index == -1:
                next
            lines[i] = line[:comment_index]

        self.lines = lines
        self.current_line_number = 0

    def current_line(self):
        return self.lines[self.current_line_number]

    def has_more_commands(self):
        return self.current_line_number < len(self.lines)

    def advance(self):
        self.current_line_number += 1

    def command_type(self):
        pass

    def symbol(self):
        # TODO... raise an error if C_COMMAND
        # otherwise returns the symbol or decimal when @Xxx or (Xxx)
        pass

    # translates assembly language into mnemonic
    def dest(self):
        # TODO... raise an error if not C_COMMAND
        # returns the dest (out of 8 possibilities)
        pass

    def comp(self):
        # TODO... returns the comp mnemonic out of 28 possibilities
        # raise an error unless C_COMMAND
        pass

    def jump(self):
        # TODO... returns the jump mnemonic out of 8 possibilities
        # raise an error unless C_COMMAND
        pass

class Code:
    # translates mnemonic (string) into binary code
    @classmethod
    def dest(mnemonic):
        pass

    def comp(mnemonic):
        pass

    def jump(mnemonic):
        pass

class SymbolTable:
    def __init__(self):
        self.hash_table = {}

    def add_entry(self, symbol: str, address: int):
        self.hash_table[symbol] = address

    def contains(self, symbol: str):
        symbol in self.hash_table

    def get_address(self, symbol):
        self.hash_table[symbol]

# save file
parser = Parser(text)

