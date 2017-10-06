import os


DATA_PATH= os.path.join(os.path.dirname(os.getcwd()),"jdBookData")

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
