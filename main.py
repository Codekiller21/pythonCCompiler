import sys
from typing import Final

import fileio


class InvalidArgsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Options:
    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.help = False

        args = sys.argv
        count = 1

        while count < len(args):
            if args[count] == "-o" or args[count] == "--output":
                count += 1
                try:
                    self.output_file = args[count]
                except IndexError:
                    raise InvalidArgsException("Need to specify a output file")
            elif args[count] == "-h" or args[count] == "--help":
                self.help = True
            else:
                self.input_file = args[count]

            count += 1


HELP: Final[str] = "Help"


def main():
    o = None
    try:
        o = Options()
    except InvalidArgsException as e:
        print(str(e), file=sys.stderr)
        exit(-1)

    if o.help:
        print(HELP)
        return
    if o.input_file is None:
        print("No input file specified", file=sys.stderr)
        exit(-1)
    if o.output_file is None:
        print("No output file specified", file=sys.stderr)
        exit(-1)

    file_data = None
    try:
        file_data = fileio.read_file(o.input_file)
    except IOError:
        print(f"Error reading file: {o.input_file}", file=sys.stderr)
        exit(-1)
    print(file_data)


if __name__ == "__main__":
    main()
