from parser import Parser
from writer import Writer

class Processor:
    @staticmethod
    def process_file(content, file_name):
        parser = Parser(content)

        writer = Writer()

        # initialize ram
        writer.initialize_pointers()

        while parser.has_more_commands():
            line = parser.current_line()
            line_number = parser.current_line_number
            if parser.current_line_type() == 'stack':
                # stack
                writer.handle_stack(line)
                parser.advance()

            elif parser.current_line_type() == 'arithmetic':
                # arithmetic
                writer.handle_arithmetic(line, line_number)
                parser.advance()
            else:
                raise Exception('unknown type')

        writer.mark_end()

        # hack_writer.print()
        writer.write_to_file('{}.asm'.format(file_name))
