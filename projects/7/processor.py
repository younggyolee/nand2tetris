from parser import Parser
from writer import HackWriter

class Processor:
    @staticmethod
    def process_file(content, file_name):
        parser = Parser(content)

        hack_writer = HackWriter()

        # initialize ram
        hack_writer.add_line('@256')
        hack_writer.add_line('D=A')
        hack_writer.add_line('@SP')
        hack_writer.add_line('M=D')

        while parser.has_more_commands():
            line = parser.current_line()
            line_number = parser.current_line_number
            if parser.current_line_type() == 'stack':
                # stack
                parser.handle_stack(line, hack_writer)
                parser.advance()

            elif parser.current_line_type() == 'arithmetic':
                # arithmetic
                parser.handle_arithmetic(line, hack_writer, line_number)
                parser.advance()
            else:
                raise Exception('unknown type')

        hack_writer.add_line('(END)')
        hack_writer.add_line('  @END')
        hack_writer.add_line('  0;JMP')

        # hack_writer.print()
        hack_writer.write_to_file('{}.asm'.format(file_name))
