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
