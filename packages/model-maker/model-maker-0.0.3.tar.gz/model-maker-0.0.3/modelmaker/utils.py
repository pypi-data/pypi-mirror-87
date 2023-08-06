import os
import shutil

def reverse_dictionary(d):
    return { v: k for k, v in d.items() }

def delete_directory(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)

def make_directory(directory, delete=False, exist_ok=True):
    if delete:
        delete_directory(directory)
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=exist_ok)
    return os.path.abspath(directory)

def files_in_folder(folder):
    return [ os.path.join(folder, n) for n in os.listdir(folder) if os.path.isfile(os.path.join(folder,n)) ]

def folders_in_folder(folder):
    return [ os.path.join(folder, n) for n in os.listdir(folder) if os.path.isdir(os.path.join(folder,n)) ]