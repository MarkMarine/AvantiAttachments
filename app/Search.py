import re
import os
import shutil
import csv

# region Description of Functions
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
# endregion


def write_log(item, log, error=""):
    with open(log, "a+") as f:
        if len(error) > 0:
            f.write("%s\t--%s\n" % (str(item), error))
        else:
            f.write("%s\n" % str(item))


def find_rev(searchtext, errorlog):  # This searches a string for the revision character
    rev_keyword = re.compile("(rev|rev |rev-|rev_|rev\.|rev\. )([a-z0-9]{1,3})", re.IGNORECASE)
    # exclude_ext = re.compile("(pdf|png|xls|doc)", re.IGNORECASE)
    exclude_ext = ["pdf", "PDF", "png", "PNG", "xls", "doc", "DOC", "iew", "ise", "isi"]
    rev_twice = re.compile("(rev).*(rev)", re.IGNORECASE)
    if rev_twice.search(searchtext) is not None:
        write_log(searchtext, errorlog, "MULTIPLE REVS IN NAME ERROR")
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
    # This splits info from the rev table file, a tab delimited text file with (PrtNum)\t(NewRev)\t(ECO for NewRev)\n
    lst = re.split(r'\t+', line.rstrip('\t'))
    return lst
    # lst[0] = Part.partnum
    # lst[1] = Part.newrev
    # lst[2] = Part.econum


def create_new_part_name(x):
    # This creates a new part name from the REV Table Line
    return str(split_rev_table_data(x)[0]) + "-REV-" + str(split_rev_table_data(x)[1])


def create_new_bom_name(x):
    return "BOM-REDLINE-" + str(split_rev_table_data(x)[0]) + "-REV-" + str(split_rev_table_data(x)[1])


def is_a_bom_redline(x):
    bom_keyword = re.compile("([\W_]BOM[\W_])", re.IGNORECASE)  # finds bom separated by a non-word or "_" char
    if bom_keyword.search(x) is not None:
        return True
    else:
        return False


def is_material_spec(x):
    ms_keyword = re.compile("([\W_]MS[\W_])", re.IGNORECASE)
    if ms_keyword.search(x) is not None:
        return True
    else:
        return False


def filter_zeros_from_rev(rev):
    return re.sub("(0)+", "", rev)


def iterate_over_list_create_objects(data, errorlog, dstdir, index_file, result_log):
    with open(data, "r+") as f:  # open the data file assuming it's in the right format
        for line in f:  # look through each line
            if len(line) > 0:
                num = split_rev_table_data(line)[0]
                rev = split_rev_table_data(line)[1]
                eco = split_rev_table_data(line)[2].rstrip('\n')
                with open(index_file, newline='', encoding='utf-8') as fi:
                    reader = csv.reader(fi, delimiter='\t')
                    for row in reader:
                        root = row[0]
                        file = row[1]
                        if num in file and eco in root and find_rev(file, errorlog) is not None \
                                and find_rev(file, errorlog) == filter_zeros_from_rev(rev) and not \
                                is_material_spec(file) and not is_a_bom_redline(file):  # TODO refactor this
                            # If the file has the part number we're looking for in it, and we can extract the rev
                            # and the rev matches what we're looking for, and it's not a mat spec or bom redline,
                            # then we'll consider it our part number + rev combo
                            src_file = os.path.join(root, file)
                            src_file_name, src_file_extension = os.path.splitext(src_file)
                            if src_file_extension == ".pdf":
                                # right now I only want to get pdf files because that is the data we have
                                # TODO pull the hardcode .pdf extension out of here and make it selectable
                                new_file_name = create_new_part_name(line) + src_file_extension  # get a new name
                                new_dst_file_name = os.path.join(dstdir, new_file_name)
                                if not os.path.exists(new_dst_file_name):
                                    shutil.copy(src_file, new_dst_file_name)
                                    write_log(("Target:\t%s-%s\ton ECO:\t%s\tfrom:\t%s\tto:\t%s" %
                                               (num, rev, eco, src_file, new_file_name)), result_log)
                                else:
                                    ii = 1
                                    while True:
                                        new_name = os.path.join(create_new_part_name(line) + "(" + str(ii) + ")" \
                                                                + src_file_extension)
                                        new_name_path = os.path.join(dstdir, new_name)
                                        if not os.path.exists(new_name_path):
                                            shutil.copy(src_file, new_name_path)
                                            write_log(("Target:\t%s-%s\ton ECO:\t%s\tfrom:\t%s\tto:\t%s" %
                                                       (num, rev, eco, src_file, new_name)), result_log)
                                            break
                                        ii += 1
                                        # extension doesn't == ".pdf"
                                        # isn't a drawing we want to copy. Don't log, it iterates over and over the list and clogs the
                                        # log file
            else:  # line length == 0
                write_log("line: %s" % line, errorlog, "Zero length line")
