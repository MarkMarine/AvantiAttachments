__author__ = 'foxma'
import mmap
import os, string, re


# Load both text files into memory

# Save a doc for loading into the item attachments for each revision:
# Line by line of the attachments data, search the REV table for the appropriate part number match. Get the new rev
# value from the REV Table (3 digit Rev) and attempt to match the part number + new rev combo.
#   If new rev == true:
#       Once you've selected the proper attachment file name, re-name the file to be <PARTNUMBER>-REV<###>.<ext> and
#       save it locally in a big folder. These will be loaded into Agile as item attachment data for each of the P/N
#       Then print full file path and name of file, and renamed file + path to the file_rename_log.txt tab delimited.
#
#   Elif 1 level up folder dir == NEW REV or similar:
#       # some of the new rev docs are stored under folders called new revs so look for that
#       same file re-name function as before
#       same print file log function as before
#
#   Else:
#       This is either a redline, supporting documentation, or it failed. Save it under a file folder named with
#       the ECO Number, and retain the name and extension. log these in the eco_attachments.txt tab delimited

# Validate that we have attachment data for each part number that was rev'd on each ECO
# line by line of the ECO Table, check if there is a file with the <PARTNUMBER>-REV<###> format for each item number on
# the ECO. If there is not, write that missing file to a log item_attachment_missing.txt with (item number, rev, ECO)

def rev_in_filename_regex(searchtext):
    rev_no_space = re.compile("(Rev|rev|REV)([A-z0-9]{1,3})")
    rev_w_space = re.compile("(Rev |rev |REV )([A-z0-9]{1,3})")
    rev_w_dash = re.compile("(Rev-|rev-|REV-)([A-z0-9]{1,3})")
    rev_w_dot = re.compile("(Rev\.|rev\.|REV\.)([A-z0-9]{1,3})")
    rev_w_dot_space = re.compile("(Rev\. |rev\. |REV\. )([A-z0-9]{1,3})")
    exclude_ext = ["pdf", "png", "xls"]
    if rev_no_space.search(searchtext) is not None:
        return rev_no_space.search(searchtext).group(2)
    elif rev_w_space.search(searchtext) is not None:
        return rev_w_space.search(searchtext).group(2)
    elif rev_w_dash.search(searchtext) is not None:
        return rev_w_dash.search(searchtext).group(2)
    elif rev_w_dot.search(searchtext) is not None:
        if rev_w_dot.search(searchtext).group(2) == exclude_ext[0]:
            return None  # TODO see if we should return something else
        elif rev_w_dot.search(searchtext).group(2) == exclude_ext[1]:
            return None
        elif rev_w_dot.search(searchtext).group(2) == exclude_ext[2]:
            return None
        else:
            return rev_w_dot.search(searchtext).group(2)
    elif rev_w_dot_space.search(searchtext) is not None:
        if rev_w_dot_space.search(searchtext).group(2) == exclude_ext[0]:
            return None  # TODO see if we should return something else
        elif rev_w_dot_space.search(searchtext).group(2) == exclude_ext[1]:
            return None
        elif rev_w_dot_space.search(searchtext).group(2) == exclude_ext[2]:
            return None
        else:
            return rev_w_dot_space.search(searchtext).group(2)
    else:
        pass  # TODO make sure pass is appropriate here



def get_newrev_from_eco_table(line):
    delimiter = '\t'
    pass  # TODO fill in this function


def new_rev_search(partnum, econum):
    pass  # TODO fill in this function


# with open('ECO_attachments.txt', 'r') as attachments, open('sample_REVT.txt', 'r') as revtable:
#     for line in attachments:
#         if rev_in_filename_regex(line) is not None:
#             print("%s   ---   %s" % (rev_in_filename_regex(line), line))
#         # new_rev_search(line)
#         # pass  # TODO Fill in this function
