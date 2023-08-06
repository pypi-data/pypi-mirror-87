import os
import sys


def n_directories_up(directory, n=1):
    
    while n > 0:
        directory = os.path.dirname(directory)
        n -= 1

    return directory


def get_root_directory_of_running_script():
    directory_scripts = os.path.realpath(sys.argv[0])
    root_directory = os.path.dirname(directory_scripts)
    return root_directory
