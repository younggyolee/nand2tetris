# read file

class Reader:
    def __init__(self):
        self.vm_text = None

    def read_text_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.vm_text = content
                print('the file has been read')
                return True
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

class HackWriter:
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

    def print(self):
        print(self.lines)


class Parser:
    def __init__(self, text):
        # text = text.replace(' ', '') # removes all white spaces
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

    def current_line(self) -> str:
        return self.lines[self.current_line_number]

    def has_more_commands(self):
        return self.current_line_number < len(self.lines)

    def advance(self):
        self.current_line_number += 1
    
    def current_line_type(self):
        l = self.current_line()
        if l.startswith('push'):
            return 'stack'
        elif l.startswith('pop'):
            return 'stack'
        else:
            return 'arithmetic'
    
    def sp_incr(self, hack_writer: HackWriter):
        hack_writer.add_line('@SP')
        hack_writer.add_line('M=M+1')

    def sp_minus_one(self, hack_writer: HackWriter):
        hack_writer.add_line('@SP')
        hack_writer.add_line('M=M-1')

    def assign_d_val_to_sp_mem(self, hack_writer: HackWriter):
        hack_writer.add_line('@SP')
        hack_writer.add_line('A=M')
        hack_writer.add_line('M=D')

    def assign_sp_mem_to_d_val(self, hack_writer: HackWriter):
        hack_writer.add_line('@SP')
        hack_writer.add_line('A=M')
        hack_writer.add_line('D=M')

    def handle_stack(self, line, hack_writer: HackWriter):
        words = line.split(' ')
        operation = words[0] # push, pop
        variable_type = words[1] # constant, local, ...
        variable = int(words[2])

        if operation == 'push':
            hack_writer.add_line('@{}'.format(variable))
            hack_writer.add_line('D=A')
            self.assign_d_val_to_sp_mem(hack_writer)
            self.sp_incr(hack_writer)
        elif operation == 'pop':
            # TODO
            pass

    def handle_arithmetic(self, line, hack_writer: HackWriter):
        if line == 'add':
            self.sp_minus_one(hack_writer)

            self.assign_d_val_to_sp_mem(hack_writer)

            self.sp_minus_one(hack_writer)

            hack_writer.add_line('@SP')
            hack_writer.add_line('A=M')
            hack_writer.add_line('M=D+M')

            self.sp_incr(hack_writer)

reader = Reader()
reader.read_text_file('./StackArithmetic/SimpleAdd/SimpleAdd.asm')
parser = Parser(reader.vm_text)

hack_writer = HackWriter()

# initialize ram
hack_writer.add_line('@256')
hack_writer.add_line('D=A')
hack_writer.add_line('@SP')
hack_writer.add_line('M=D')

while parser.has_more_commands():
    line = parser.current_line()
    if parser.current_line_type() == 'stack':
        # stack
        parser.handle_stack(line, hack_writer)
        parser.advance()

    elif parser.current_line_type() == 'arithmetic':
        # arithmetic
        parser.handle_arithmetic(line, hack_writer)
        parser.advance()

hack_writer.add_line('(END)')
hack_writer.add_line('  @END')
hack_writer.add_line('  0;JMP')

hack_writer.print()
hack_writer.write_to_file('simple_add.asm')


