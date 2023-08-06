import subprocess


def is_windows_cmd():
    p = subprocess.run("true", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return p.returncode == 1
