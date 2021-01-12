from typing import Dict, Tuple, Optional
import fileio


class LineReader:
    def __init__(self, data: str):
        self.data = data
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self) -> str:
        tok = ""
        try:
            while self.data[self.count] != "\n":
                tok += self.data[self.count]
                self.count += 1
            self.count += 1
        except IndexError:
            if tok != "":
                return tok
            else:
                raise StopIteration

        return tok


class PreProcessException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def get_statement_type(line: str) -> Tuple[str, int]:
    count = 1
    tok = ""

    while count < len(line) and line[count] != " ":
        tok += line[count]
        count += 1

    return tok, count


def pre_process(data: str, defines: Optional[Dict[str, Optional[str]]]) -> str:
    lr = LineReader(data)
    output = ""
    if defines is None:
        defines: Dict[str, Optional[str]] = {}
    line = ""
    saving = True

    try:
        for line in lr:
            if line == "":
                continue
            # Checks for preprocessor statements
            if line[0] == "#":
                statement_type, count = get_statement_type(line)
                # Parses and runs define statements
                if saving and statement_type == "define":
                    name = ""
                    count += 1
                    try:
                        while line[count] != " ":
                            name += line[count]
                            count += 1
                    except IndexError:
                        defines[name] = None
                        continue
                    value = " "
                    while count < len(line):
                        value += line[count]
                        count += 1
                    value += " "
                    defines[name] = value
                # End define
                elif saving and statement_type == "ifdef":
                    name = ""
                    count += 1
                    while count < len(line) and line[count] != " ":
                        name += line[count]
                        count += 1
                    found = False
                    for key in defines.keys():
                        if name == key:
                            found = True
                            break
                    if found:
                        saving = True
                    else:
                        saving = False
                # End ifdef
                elif saving and statement_type == "ifndef":
                    name = ""
                    count += 1
                    while count < len(line) and line[count] != " ":
                        name += line[count]
                        count += 1
                    not_found = True
                    for key in defines.keys():
                        if name == key:
                            not_found = False
                            break
                    if not_found:
                        saving = True
                    else:
                        saving = False
                # End ifndef
                elif statement_type == "endif":
                    saving = True
                elif statement_type == "undef":
                    name = ""
                    count += 1
                    while count < len(line) and line[count] != " ":
                        name += line[count]
                        count += 1
                    try:
                        del defines[name]
                    except KeyError:
                        pass
                # End undef
                elif saving and statement_type == "include":
                    try:
                        while line[count] != "\"" and line[count] != "<":
                            count += 1
                    except IndexError:
                        raise PreProcessException(
                            f"Need to specify file inside {{\" \"}} or {{< >}}, on include: {line}"
                        )
                    name = ""
                    if line[count] == "\"":
                        count += 1
                        while line[count] != "\"":
                            name += line[count]
                            count += 1
                        try:
                            file_data = fileio.read_file(name)
                        except IOError:
                            raise PreProcessException(f"Couldn't load file: {name} in include: {line}")
                        output += pre_process(file_data, defines) + "\n"
                    else:
                        raise PreProcessException("Have not implemented includes with {{< >}} yet")
                # End include
            else:
                if saving:
                    output += line + "\n"
    except IndexError:
        raise PreProcessException(f"Unexpected end of pre process statement on: {line}")

    return output
