from argparse import ArgumentDefaultsHelpFormatter

class ArgumentDefaultsSmartHelpFormatter(
        ArgumentDefaultsHelpFormatter):
    def _split_lines(self, text, width):
        lines = text.split('\\newline')
        formatted_lines = []
        for line in lines:
            formatted_lines.extend(super()._split_lines(line, width))
        return [line.replace('\\tab', ' ' * 4)
                for line in formatted_lines]
