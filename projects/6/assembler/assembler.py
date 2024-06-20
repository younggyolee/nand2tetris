# read file
def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

# parser
class Parser:
    COMMAND_TYPES = {
        'A_COMMAND': 'A_COMMAND',
        'C_COMMAND': 'C_COMMAND',
        'L_COMMAND': 'L_COMMAND'
    }

    def __init__(self, text):
        text = text.replace(' ', '') # removes all white spaces
        lines = text.split('\n')

        # remove comments
        for i, line in enumerate(lines):
            comment_index = line.find('//')
            if comment_index == -1:
                continue
            lines[i] = line[:comment_index]

        lines = [x for x in lines if len(x) > 0] # removes empty lines

        self.lines = lines
        self.current_line_number = 0

    def current_line(self):
        return self.lines[self.current_line_number]

    def has_more_commands(self):
        return self.current_line_number < len(self.lines)

    def advance(self):
        self.current_line_number += 1

    def command_type(self):
        if self.current_line()[0] == '@':
            return 'A_COMMAND'
        elif self.current_line()[0] == '(':
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        # returns the symbol or decimal when @Xxx or (Xxx)
        if self.command_type() == Parser.COMMAND_TYPES['C_COMMAND']:
            raise Exception

        if self.command_type() == Parser.COMMAND_TYPES['A_COMMAND']:
            end = len(self.current_line())
        else:
            end = len(self.current_line()) - 1
        return self.current_line()[1 : end]

    def is_symbol_decimal(self):
        return self.symbol(self).isdigit()

    # translates assembly language into mnemonic
    def dest(self):
        # should return one of [null, M, D, DM, A, AM, AD, ADM]
        if self.command_type() != Parser.COMMAND_TYPES['C_COMMAND']:
            raise Exception

        if '=' not in self.current_line():
            return None
        else:
            equal_sign_index = self.current_line().find('=')
            return self.current_line()[:equal_sign_index]

    def comp(self):
        # should return the comp mnemonic out of 28 possibilities

        if self.command_type() != Parser.COMMAND_TYPES['C_COMMAND']:
            raise Exception

        equal_sign_index = self.current_line().find('=')
        semi_colon_index = self.current_line().find(';')

        start = max(equal_sign_index + 1, 0)
        end = len(self.current_line()) if semi_colon_index == -1 else semi_colon_index

        return self.current_line()[start : end]

    def jump(self):
        # should return the jump mnemonic out of 8 possibilities
        if self.command_type() != Parser.COMMAND_TYPES['C_COMMAND']:
            raise Exception

        semi_colon_index = self.current_line().find(';')
        if semi_colon_index == -1:
            return None
        else:
            return self.current_line()[semi_colon_index + 1 :]

class Code:
    # translates mnemonic (string) into binary code
    @classmethod
    def dest(cls, mnemonic):
        match mnemonic:
            case None:
                return '000'
            case 'M':
                return '001'
            case 'D':
                return '010'
            case 'DM' | 'MD':
                return '011'
            case 'A':
                return '100'
            case 'AM':
                return '101'
            case 'AD':
                return '110'
            case 'ADM':
                return '111'
            case _:
                raise Exception

    @classmethod
    def comp(cls, mnemonic):
        if 'M' in mnemonic:
            a = '1'
        else:
            a = '0'
        c = None
        match mnemonic:
            case '0':
                c = '101010'
            case '1':
                c = '111111'
            case '-1':
                c = '111010'
            case 'D':
                c = '001100'
            case 'A' | 'M':
                c = '110000'
            case '!D':
                c = '001101'
            case '!A' | '!M':
                c = '110001'
            case '-D':
                c = '001111'
            case '-A' | '-M':
                c = '110011'
            case 'D+1':
                c = '011111'
            case 'A+1' | 'M+1':
                c = '110111'
            case 'D-1':
                c = '001110'
            case 'A-1' | 'M-1':
                c = '110010'
            case 'D+A' | 'D+M':
                c = '000010'
            case 'D-A' | 'D-M':
                c = '010011'
            case 'A-D' | 'M-D':
                c = '000111'
            case 'D&A' | 'D&M':
                c = '000000'
            case 'D|A' | 'D|M':
                c = '010101'
            case _:
                raise Exception
        return a + c

    @classmethod
    def jump(cls, mnemonic):
        match mnemonic:
            case None:
                return '000'
            case 'JGT':
                return '001'
            case 'JEQ':
                return '010'
            case 'JGE':
                return '011'
            case 'JLT':
                return '100'
            case 'JNE':
                return '101'
            case 'JLE':
                return '110'
            case 'JMP':
                return '111'
            case _:
                raise Exception

class SymbolTable:
    def predefined(self):
        hash_table = {
            'SCREEN': 16384,
            'KBD': 24576,
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4
        }

        # R0~R15
        for i in range(16):
            key = 'R%d' % i
            hash_table[key] = i

        return hash_table

    def __init__(self):
        self.hash_table = self.predefined()

    def add_entry(self, symbol: str, address: int):
        self.hash_table[symbol] = address
        return True

    def contains(self, symbol: str):
        return symbol in self.hash_table

    def get_address(self, symbol):
        return self.hash_table[symbol]

# save file

class BinaryWriter:
    def __init__(self):
        self.lines = []

    def add_line(self, text):
        self.lines.append(text)

    def lines(self):
        self.lines

    def write_to_file(self, filename):
        with open(filename, 'w') as file:
            # Loop through each element in the array
            for element in self.lines:
                # Write the element to the file followed by a newline
                file.write(element + '\n')

def first_pass(text, symbol_table: SymbolTable):
    # handle symbols

    # 2. label symbols (Xxx) => remember
    line_number = 0
    parser = Parser(text)
    while parser.has_more_commands():
        if parser.command_type() == 'L_COMMAND':
            # remember the line number
            symbol_table.add_entry(parser.symbol(), line_number)

        else:
            line_number += 1

        parser.advance()

def second_pass(text, symbol_table: SymbolTable, file_path):
    binary_writer = BinaryWriter()
    parser = Parser(text)
    address_for_variable = 16

    while parser.has_more_commands():
        match parser.command_type():
            case 'A_COMMAND':
                # 1. predefined symbols = @R0 => replace with predefined values
                # 2. label symbols = @Xxx => replace with the line number we remember
                # 3. variable symbols = @i => replace with address, starting from 16
                symbol = parser.symbol()
                if not symbol.isdigit():
                    if symbol_table.contains(symbol):
                        # 1. predefined or 2. label
                        symbol = symbol_table.get_address(symbol)
                    else:
                        # 3. variable symbol
                        symbol_table.add_entry(symbol, address_for_variable)
                        symbol = address_for_variable
                        address_for_variable += 1

                bin_line = format(int(symbol), '#018b')[2:]
                binary_writer.add_line(bin_line)
            case 'C_COMMAND':
                dest = Code.dest(parser.dest())
                comp = Code.comp(parser.comp())
                jump = Code.jump(parser.jump())
                bin_line = '111' + comp + dest + jump
                binary_writer.add_line(bin_line)
            # case 'L_COMMAND':
            #     symbol = parser.symbol()
            #     bin_line = ''

        parser.advance()

    binary_writer.write_to_file(file_path.replace('.asm', '') + '.hack')

def run(file_path):
    symbol_table = SymbolTable()
    text = read_text_file(file_path)
    first_pass(text, symbol_table)
    # print(symbol_table.hash_table)
    second_pass(text, symbol_table, file_path)

for file_path in [
    '../add/Add.asm',
    '../max/Max.asm',
    '../max/MaxL.asm',
    '../pong/Pong.asm',
    '../pong/PongL.asm',
    '../rect/Rect.asm',
    '../rect/RectL.asm'
]:
    run(file_path)
