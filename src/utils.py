import os
import glob

def DeleteImages():
    for file in glob.glob('img/*'):
        os.remove(file)