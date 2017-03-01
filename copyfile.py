import os
import shutil
import logging


def touch(fname, times=None):
    fpath, f = os.path.split(fname)
    if not os.path.exists(fpath):
        os.makedirs(fpath)

    with open(fname, 'a'):
        os.utime(fname, times)

def copyFile(src, dest):
    """Copies a source file to a destination whose path may not yet exist.

    Keyword arguments:
    src -- Source path to a file (string)
    dest -- Path for destination file (also a string)
    """
    #Src Exists?
    try:
        if os.path.isfile(src):
            dpath, dfile = os.path.split(dest)

            if not os.path.isdir(dpath):
                os.makedirs(dpath)

            if not os.path.exists(dest):
                touch(dest)
            try:
                shutil.copy2(src, dest)
            # eg. src and dest are the same file
            except shutil.Error as e:
                logging.exception('Error: %s' % e)
            # eg. source or destination doesn't exist
            except IOError as e:
                logging.exception('Error: %s' % e.strerror)
    except:
        logging.exception('Error: src to copy does not exist.')
