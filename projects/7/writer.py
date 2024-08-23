
class Writer:
    # write to an output file
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


    # high level methods
    def handle_stack(self, line):
        words = line.split(' ')
        operation = words[0] # push, pop
        variable_type = words[1] # constant, local, ...
        variable = int(words[2])

        if operation == 'push':
            self.add_line('@{}'.format(variable))
            self.add_line('D=A')
            self.assign_d_val_to_sp_mem()
            self.sp_incr()
        elif operation == 'pop':
            # TODO
            pass


    def handle_arithmetic(self, line, line_number):
        if line in ['neg', 'not']:
            self.sp_minus_one()
            self.assign_sp_mem_to_d_val()
            if line == 'neg':
                self.add_line('M=-M')
            elif line == 'not':
                self.add_line('M=!M')
            self.sp_incr()
            return

        self.sp_minus_one()

        self.assign_sp_mem_to_d_val()

        self.sp_minus_one()

        self.add_line('@SP')
        self.add_line('A=M')

        if line in ['add', 'sub']:
            if line == 'add':
                self.add_line('M=D+M')
            elif line == 'sub':
                self.add_line('M=M-D')
        elif line in ['eq', 'lt', 'gt']:
            if line == 'eq':
                self.add_line('D=M-D')
                self.add_line('@EQ{}'.format(line_number))
                self.add_line('D;JEQ')

                self.add_line('@NEQ{}'.format(line_number))
                self.add_line('0;JMP')

            elif line == 'lt':
                self.add_line('D=M-D')
                self.add_line('@EQ{}'.format(line_number))
                self.add_line('D;JLT')

                self.add_line('@NEQ{}'.format(line_number))
                self.add_line('0;JGE')

            elif line == 'gt':
                self.add_line('D=M-D')
                self.add_line('@EQ{}'.format(line_number))
                self.add_line('D;JGT')

                self.add_line('@NEQ{}'.format(line_number))
                self.add_line('0;JLE')

            self.add_line('(EQ{})'.format(line_number))
            self.assign_minus_one_to_sp_mem(self)
            self.add_line('  @FINISHED{}'.format(line_number))
            self.add_line('  0; JMP')

            self.add_line('(NEQ{})'.format(line_number))
            self.assign_0_to_sp_mem(self)

            self.add_line('(FINISHED{})'.format(line_number))
        elif line in ['and', 'or']:
            if line == 'and':
                self.add_line('D=D&M')

            elif line == 'or':
                self.add_line('D=D|M')

            self.add_line('M=D')

        self.sp_incr()

    def mark_end(self):
        self.add_line('(END)')
        self.add_line('  @END')
        self.add_line('  0;JMP')

    def initialize_pointers(self):
        self.add_line('@256')
        self.add_line('D=A')
        self.add_line('@SP')
        self.add_line('M=D')

    # common logics
    def sp_incr(self):
        self.add_line('@SP')
        self.add_line('M=M+1')

    def sp_minus_one(self):
        self.add_line('@SP')
        self.add_line('M=M-1')

    def assign_d_val_to_sp_mem(self):
        self.add_line('@SP')
        self.add_line('A=M')
        self.add_line('M=D')

    def assign_sp_mem_to_d_val(self):
        self.add_line('@SP')
        self.add_line('A=M')
        self.add_line('D=M')

    def assign_0_to_sp_mem(self):
        self.add_line('@SP')
        self.add_line('A=M')
        self.add_line('M=0')

    def assign_minus_one_to_sp_mem(self):
        self.add_line('@SP')
        self.add_line('A=M')
        self.add_line('M=-1')

