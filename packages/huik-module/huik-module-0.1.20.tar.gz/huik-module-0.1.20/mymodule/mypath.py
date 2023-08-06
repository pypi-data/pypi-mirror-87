import os 

def mkdirs(*args):
    """
    check if the folder exists. If not, make the folder. 
    """
    for p in args:
        if not os.path.isdir(p):
            os.mkdir(p) 
    