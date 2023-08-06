import os
import shutil
import stat


def rmdir(dir_to_delete: str):
    def on_rm_error(func, path, exc_info):
        # path contains the path of the file that couldn't be removed
        # let's just assume that it's read-only and unlink it.
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    shutil.rmtree(dir_to_delete, onerror=on_rm_error)
