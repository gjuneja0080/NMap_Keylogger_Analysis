import pynput

from pynput.keyboard import Key, Listener
#vanilla
import logging

#make a logfile
log_dir1 = ""
log_dir2 = ""

def setup_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s, %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)


    l.setLevel(level)
    l.addHandler(fileHandler)



setup_logger('log1', log_dir1 + "key_PandalogPress.csv")
setup_logger('log2', log_dir2 + "key_PandalogRelease.csv")
logger_1 = logging.getLogger('log1')
logger_2 = logging.getLogger('log2')


def on_press(key):
    if (str(key) == 'Key.shift' or str(key) == 'Key.caps_lock' or str(key) == 'Key.shift_r'):
        logger_1.disabled
    else:
        logger_1.info(str(key))

def on_release(key):
    if (str(key) == 'Key.shift' or str(key) == 'Key.caps_lock' or str(key) == 'Key.shift_r'):
        logger_2.disabled
    else:
        logger_2.info(str(key))
        if key == Key.esc:
            # Stop listener
            return False


#this says, Listener is on
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
