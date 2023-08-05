import os
import shutil


class CondaExecutablePathFinder:
    def find(self):
        homedir = os.path.expanduser("~")

        if shutil.which("conda"):
            return shutil.which("conda")

        conda_paths = {
            f"{homedir}/Miniconda3/Library/bin/conda.bat": f"{homedir}/Miniconda3",
            f"{homedir}/Anaconda3/Library/bin/conda.bat": f"{homedir}/Anaconda3",
            f"{homedir}/AppData/Local/Continuum/miniconda3/condabin/conda.bat": f"{homedir}/AppData/Local/Continuum/miniconda3",
            f"{homedir}/AppData/Local/Continuum/anaconda3/condabin/conda.bat": f"{homedir}/AppData/Local/Continuum/anaconda3",
            f"{homedir}/miniconda3/bin/conda": f"{homedir}/miniconda3",
            f"{homedir}/anaconda3/bin/conda": f"{homedir}/anaconda3",
            f"{homedir}/miniconda/bin/conda": f"{homedir}/miniconda",
            f"{homedir}/anaconda/bin/conda": f"{homedir}/anaconda",
            "c:/Miniconda3/Library/bin/conda.bat": "c:\\Miniconda3",
            "c:/Miniconda/Library/bin/conda.bat": "c:\\Miniconda",
            "c:/Anaconda3/Library/bin/conda.bat": "c:\\Anaconda3",
            "c:/Anaconda/Library/bin/conda.bat": "c:\\Anaconda",
        }

        for conda_executable_path, conda_installation_dir in conda_paths.items():
            if os.path.isfile(conda_executable_path):
                return conda_executable_path

        raise Exception("Unable to find Conda executable, exiting...")
