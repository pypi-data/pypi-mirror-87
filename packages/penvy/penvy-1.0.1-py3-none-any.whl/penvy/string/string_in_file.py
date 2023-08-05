def file_contains_string(search: str, path: str):
    with open(path) as f:
        return search in f.read()
