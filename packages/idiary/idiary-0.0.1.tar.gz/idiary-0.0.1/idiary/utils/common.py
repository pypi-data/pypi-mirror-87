import logging
import shutil
import os

def set_logger(name):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    return log

def copy_files(old_path, new_path, name):
    log = set_logger(name)
    log.info("New path:{}\nOld path:{}".format(new_path, old_path))
    filelist = os.listdir(old_path)
    for file in filelist:
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)
        shutil.copy(src, dst)
        log.info("Copy from {} to {}".format(src, dst))
    log.info("Finish Copying.")
