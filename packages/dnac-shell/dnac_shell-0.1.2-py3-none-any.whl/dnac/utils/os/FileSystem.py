import contextlib
import os
from tempfile import gettempdir
from shutil import rmtree
import shutil


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class FileSystem:
    def __init__(self):
        pass

    @staticmethod
    def maketempdir():
        tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
        os.makedirs(tmp)
        return tmp

    @staticmethod
    def cleanup(folder):
        if folder:
            rmtree(folder, ignore_errors=True)

    @staticmethod
    def is_valid_file(folderx, filex):
        if folderx and os.path.isdir(folderx):
            os.chdir(folderx)
            return True if os.path.exists(filex) and os.path.isfile(filex) and (os.path.getsize(filex) > 0) else False
        return False

    @staticmethod
    def is_file_readable(fnm):
        return os.path.exists(fnm) and os.path.isfile(fnm) and (os.path.getsize(fnm) > 0) and os.access(fnm, os.R_OK)

    @staticmethod
    def is_file_writable(fnm):
        if os.path.exists(fnm):
            # path exists
            if os.path.isfile(fnm):  # is it a file or a dir?
                # also works when file is a link and the target is writable
                return os.access(fnm, os.W_OK)
            else:
                return False  # path is a dir, so cannot write as a file
        # target does not exist, check perms on parent dir
        pdir = os.path.dirname(fnm)
        if not pdir: pdir = '.'
        # target is creatable if parent dir is writable
        return os.access(pdir, os.W_OK)

    @staticmethod
    def force_delete_file(fnm):
        with contextlib.suppress(FileNotFoundError):
            os.remove(fnm)

    @staticmethod
    def move(fnm_from, fnm_target):
        # Move a file from one path to another
        shutil.move(fnm_from, fnm_target)
