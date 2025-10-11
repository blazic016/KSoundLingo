import os
import sys
import shutil
import tempfile


def validate_file(input_file: str, ext: str):
    """
    Validates that a file exists and has the expected extension.
    
    Args:
        input_file (str): Path to the input file.
        ext (str): Expected file extension (e.g., '.txt', '.md').

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file does not have the correct extension.
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"File '{input_file}' doesn't exist!")

    if not input_file.lower().endswith(ext.lower()):
        raise ValueError(
            f"File '{input_file}' isn't {ext}! Please provide a file with extension {ext}."
        )
        
        

def get_resource_path(rel_path: str) -> str:
    """
    Returns absolute path to resource, compatible with PyInstaller.

    If the app is bundled into a single executable using PyInstaller,
    resources are extracted to a temporary folder (`sys._MEIPASS`).
    Otherwise, uses current working directory.
    """
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)


# TODO: sredi da se svuda koristi Path objekat, a ne string kao trenutno.
def ensure_dir(path: str):
    """
    Creates the directory if it does not exist.
    Equivalent to: os.makedirs(path, exist_ok=True)
    """
    os.makedirs(path, exist_ok=True)
    
    
def remove_dir_if_exists(path: str):
    """
    Removes a directory and all its contents if it exists.
    Equivalent to:
        if os.path.exists(path):
            shutil.rmtree(path)
    """
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Removed directory : {path}")
        
        
def create_temp_dir(prefix="kslingo_") -> str:
    """
    Creates a unique temporary directory and returns its path.
    Default location is system temp (e.g., /tmp/...).
    """
    return tempfile.mkdtemp(prefix=prefix)