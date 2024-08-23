from parser import Parser
from writer import Writer

class Processor:
    @staticmethod
    def process_file(content, new_file_path):
        parser = Parser(content)
        writer = Writer()

        writer.initialize_pointers()

        while parser.has_more_commands():
            line = parser.current_line()
            line_number = parser.current_line_number
            writer.add_line(f'//{line}') # for readability
            if parser.current_line_type() == 'stack':
                writer.handle_stack(line)
                parser.advance()
            elif parser.current_line_type() == 'arithmetic':
                writer.handle_arithmetic(line, line_number)
                parser.advance()
            else:
                raise Exception('unknown type')
            writer.add_line('')

        writer.mark_end()

        writer.write_to_file(new_file_path)
