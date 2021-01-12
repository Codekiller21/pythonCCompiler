import sys
from typing import Final

import fileio
import preprocessor
import lexical


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

    pre = None
    try:
        pre = preprocessor.pre_process(file_data, None)
    except preprocessor.PreProcessException as e:
        print(str(e), file=sys.stderr)
        exit(-1)
    print(pre, end="\n\n\n")

    toks = None
    try:
        toks = lexical.tokenize(pre + "\n\n")
    except lexical.TokenizerException as e:
        print(str(e), file=sys.stderr)
        exit(-1)
    except IndexError:
        print("Unexpected end of file in tokenizing")
        exit(-1)
    for t in toks:
        print(str(t))


if __name__ == "__main__":
    main()
