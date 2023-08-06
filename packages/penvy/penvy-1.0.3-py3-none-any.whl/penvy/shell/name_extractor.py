def extract_shell_name(shell_name: str):
    start_index = shell_name.rfind("/") + 1
    return shell_name[start_index:]
