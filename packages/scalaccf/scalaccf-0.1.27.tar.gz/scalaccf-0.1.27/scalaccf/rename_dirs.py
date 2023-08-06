import logging
import os
from scalaccf.formatter import Formatter


def rename_dirs(path, mode):
    print(path)
    for file in os.listdir(path):
        d = os.path.join(path, file)
        if os.path.isdir(d):
            print(file)
            rename_dirs(d, mode)
            expected = Formatter.to_lower(file)
            if expected != file:
                logging.warning(f'{file}: Wrong naming for package. Expected {expected}, but found {file}')
                if mode == 'trace':
                    os.rename(d, os.path.join(path, expected))
