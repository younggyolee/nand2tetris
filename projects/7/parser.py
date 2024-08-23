from writer import HackWriter

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

    def assign_0_to_sp_mem(self, hack_writer: HackWriter):
        hack_writer.add_line('@SP')
        hack_writer.add_line('A=M')
        hack_writer.add_line('M=0')

    def assign_minus_one_to_sp_mem(self, hack_writer: HackWriter):
        hack_writer.add_line('@SP')
        hack_writer.add_line('A=M')
        hack_writer.add_line('M=-1')

    # def assign_val_to_sp_mem(self, val, hack_writer: HackWriter):
    #     if val >= 0:
    #         hack_writer.add_line('@{}'.format(val))
    #         hack_writer.add_line('D=A')
    #         hack_writer.add_line('@SP')
    #         hack_writer.add_line('A=M')
    #         hack_writer.add_line('M=D')
    #     else:
    #         hack_writer.add_line('@{}'.format(-val))
    #         hack_writer.add_line('D=A')
    #         hack_writer.add_line('@SP')
    #         hack_writer.add_line('A=M')
    #         hack_writer.add_line('M=D')
    #         hack_writer.add_line('M=-M')


    def handle_arithmetic(self, line, hack_writer: HackWriter, line_number):
        if line in ['neg', 'not']:
            self.sp_minus_one(hack_writer)
            self.assign_sp_mem_to_d_val(hack_writer)
            if line == 'neg':
                hack_writer.add_line('M=-M')
            elif line == 'not':
                hack_writer.add_line('M=!M')
            self.sp_incr(hack_writer)
            return

        self.sp_minus_one(hack_writer)

        self.assign_sp_mem_to_d_val(hack_writer)

        self.sp_minus_one(hack_writer)

        hack_writer.add_line('@SP')
        hack_writer.add_line('A=M')

        if line in ['add', 'sub']:
            if line == 'add':
                hack_writer.add_line('M=D+M')
            elif line == 'sub':
                hack_writer.add_line('M=M-D')
        elif line in ['eq', 'lt', 'gt']:
            if line == 'eq':
                hack_writer.add_line('D=M-D')
                hack_writer.add_line('@EQ{}'.format(line_number))
                hack_writer.add_line('D;JEQ')

                hack_writer.add_line('@NEQ{}'.format(line_number))
                hack_writer.add_line('0;JMP')

            elif line == 'lt':
                hack_writer.add_line('D=M-D')
                hack_writer.add_line('@EQ{}'.format(line_number))
                hack_writer.add_line('D;JLT')

                hack_writer.add_line('@NEQ{}'.format(line_number))
                hack_writer.add_line('0;JGE')

            elif line == 'gt':
                hack_writer.add_line('D=M-D')
                hack_writer.add_line('@EQ{}'.format(line_number))
                hack_writer.add_line('D;JGT')

                hack_writer.add_line('@NEQ{}'.format(line_number))
                hack_writer.add_line('0;JLE')

            hack_writer.add_line('(EQ{})'.format(line_number))
            self.assign_minus_one_to_sp_mem(hack_writer)
            hack_writer.add_line('  @FINISHED{}'.format(line_number))
            hack_writer.add_line('  0; JMP')

            hack_writer.add_line('(NEQ{})'.format(line_number))
            self.assign_0_to_sp_mem(hack_writer)

            hack_writer.add_line('(FINISHED{})'.format(line_number))
        elif line in ['and', 'or']:
            if line == 'and':
                hack_writer.add_line('D=D&M')

            elif line == 'or':
                hack_writer.add_line('D=D|M')

            hack_writer.add_line('M=D')

        self.sp_incr(hack_writer)