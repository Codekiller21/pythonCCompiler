def read_file(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()
