import re
import os
import shutil
import datetime

# Load both text files into memory

# Save a doc for loading into the item attachments for each revision:
# Line by line of the rev table, search the attachments for the appropriate part number + rev match. Get the new rev
# value from the REV Table (3 digit Rev) and attempt to match the part number + new rev combo.
# If new rev == true:
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
# errorlog = os.path.normpath("c:/users/foxma/documents/github/avantiattachments/results/manual_fix_required.txt")


def write_error_log(item, error, errorlog):
    with open(errorlog, "a+") as fix_file:
        fix_file.write("%s\t--%s\n" % (str(item), error))


def find_rev(searchtext, errorlog):  # This searches a string for the revision character
    rev_keyword = re.compile("(rev|rev |rev-|rev_|rev\.|rev\. )([a-z0-9]{1,3})", re.IGNORECASE)
    # exclude_ext = re.compile("(pdf|png|xls|doc)", re.IGNORECASE)
    exclude_ext = ["pdf", "PDF", "png", "PNG", "xls", "doc", "DOC", "iew", "ise", "isi"]
    rev_twice = re.compile("(rev).*(rev)", re.IGNORECASE)
    if rev_twice.search(searchtext) is not None:
        write_error_log(searchtext, "MULTIPLE REV ERROR", errorlog)  # write searchtext to a log file of manual fixes
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


def split_rev_table_data(line):
    lst = re.split(r'\t+', line.rstrip('\t'))
    return lst
    # lst[0] = Part.partnum
    # lst[1] = Part.newrev
    # lst[2] = Part.econum


def create_new_part_name(data):
    new_obj_name = str(split_rev_table_data(data)[0]) + "-REV-" + str(split_rev_table_data(data)[1])
    return new_obj_name


def iterate_over_list_create_objects(data, path, errorlog, dstdir):
    with open(data, "r+") as f:  # open the data file assuming it's in the right format
        for line in f:  # look through each line
            if len(line) > 0:
                num = split_rev_table_data(line)[0]
                rev = split_rev_table_data(line)[1]
                eco = split_rev_table_data(line)[2].rstrip('\n')
                print(num + " " + rev + " at " + str(datetime.datetime.now()))
                for root, dirs, files in os.walk(path):
                    if eco in root:
                        for file in files:
                            if num in file and find_rev(file, errorlog) in rev:
                                src_file = os.path.join(root, file)
                                shutil.copy(src_file, dstdir)
                                src_file_name, src_file_extension = os.path.splitext(src_file)
                                new_file_name = create_new_part_name(line) + src_file_extension
                                old_dst_file_name = dstdir + "\\" + file
                                new_dst_file_name = os.path.join(dstdir, new_file_name)
                                os.rename(old_dst_file_name, new_dst_file_name)
                                print(create_new_part_name(line) + " from: " + os.path.join(root, file))






# def generate_sample_index(attachments, revs):
# with open(attachments, 'r') as attachment_index, open(revs, 'r') as revtable:
#         for line in attachment_index:
#             if find_rev(line, errorlog) is not None:
#                 print("%s   ---   %s" % (find_rev(line, errorlog), line))
#                 # pass  # TODO Fill in this function
