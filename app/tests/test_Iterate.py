__author__ = 'foxma'

from app.Search import *

data = os.path.normpath("c:/users/foxma/documents/github/avantiattachments/indexes/ItemNewRevW_O_sftwr.txt")
# path = os.path.normpath("C:/AVANTI/")
error_log = os.path.normpath("c:/users/foxma/documents/github/avantiattachments/results/error_log.txt")
results_log = os.path.normpath("c:/users/foxma/documents/github/avantiattachments/results/results_log.txt")
dstdir = os.path.normpath("c:/users/foxma/documents/github/avantiattachments/results")
index_file = os.path.normpath("c:/users/foxma/documents/github/avantiattachments/indexes/local_att_delim.txt")
debug = True
debug_log = os.path.normpath("c:/users/foxma/documents/github/avantiattachments/results/debug_log.txt")
print(iterate_over_list_create_objects(data, error_log, dstdir, index_file, results_log, debug, debug_log))