
import re

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

def find_rev(searchtext, errorlog):  # This searches a string for the revision character
    rev_keyword = re.compile("(rev|rev |rev-|rev_|rev\.|rev\. )([a-z0-9]{1,3})", re.IGNORECASE)
    # exclude_ext = re.compile("(pdf|png|xls|doc)", re.IGNORECASE)
    exclude_ext = ["pdf", "PDF", "png", "PNG", "xls", "doc", "DOC", "iew", "ise", "isi"]
    rev_twice = re.compile("(rev).*(rev)", re.IGNORECASE)
    if rev_twice.search(searchtext) is not None:
        # write searchtext to a log file of manual fixes
        with open(errorlog, "a+") as fix_file:
            fix_file.write("%s\t--MULTIPLE REV ERROR\n" % str(searchtext))
        return None
    elif rev_keyword.search(searchtext) is not None:
        exclude = False
        for x in exclude_ext:
            if rev_keyword.search(searchtext).group(2) == x:  # TODO fix exclude list search
                exclude = True
        if not exclude:
            return rev_keyword.search(searchtext).group(2)
        else:
            return None
    else:
        pass  # TODO make sure pass is appropriate here


def get_new_rev(searchtext):  # This searches the index for the
    delimiter = '\t'
    pass  # TODO fill in this function


def new_rev_search(partnum, econum):
    pass  # TODO fill in this function


errorlog = "results/manual_fix_required.txt"

def generate_sample_index(attachments, revs):
    with open(attachments, 'r') as attachment_index, open(revs, 'r') as revtable:
        for line in attachment_index:
            if find_rev(line, errorlog) is not None:
                print("%s   ---   %s" % (find_rev(line, errorlog), line))
            # pass  # TODO Fill in this function
