import csv
import re
import os
import shutil
import logging


def filter_zeros_from_rev(rev):
    return re.sub("(0)+", "", rev)


def is_new_rev_folder(directory):
    new_rev_folder_regex = re.compile("(NEW REV)", re.IGNORECASE)
    if new_rev_folder_regex.search(directory) is not None:
        return True
    else:
        return False


def return_rev_from_file_name(file_name):
    # This searches a string for the revision character
    rev_keyword = re.compile("(rev[ \-_\.]*?)((?!isi|ise|iew|pdf)[a-z0-9]{1,3})", re.IGNORECASE)
    if rev_keyword.search(file_name) is not None:
        logging.debug("return_rev_from_file_name\t%s\t%s" % (file_name, rev_keyword.search(file_name).group(2)))
        return rev_keyword.search(file_name).group(2)
    else:
        logging.debug("no rev in file_name\t%s" % file_name)


def find_multiple_revs_in_file_name(file_name):
    rev_twice = re.compile("(rev).*(rev)", re.IGNORECASE)
    if rev_twice.search(file_name) is not None:
        logging.error("MULTIPLE REVS IN NAME ERROR\t%s" % file_name)
        return True
    else:
        return False


def split_rev_table_data(rev_table_line):
    # This splits info from the rev table file, a tab delimited text file with (PrtNum)\t(NewRev)\t(ECO for NewRev)\n
    lst = re.split(r'\t+', rev_table_line.rstrip('\t'))
    return lst
    # lst[0] = partnum
    # lst[1] = newrev
    # lst[2] = econum


def create_new_part_name(rev_table_line):
    # This creates a new part name from the REV Table Line
    return str(split_rev_table_data(rev_table_line)[0]) + "-REV-" + str(split_rev_table_data(rev_table_line)[1])


def is_a_bom_redline(file_name):
    bom_keyword = re.compile("([\W_]BOM[\W_])", re.IGNORECASE)  # finds bom separated by a non-word or "_" char
    redline_keyword = re.compile("RED LINE", re.IGNORECASE)
    if bom_keyword.search(file_name) is not None or redline_keyword.search(file_name) is not None:
        return True
    else:
        return False


def is_material_spec(file_name):
    ms_keyword = re.compile("([\W_]MS[\W_])", re.IGNORECASE)
    ms_start_keyword = re.compile("(MS[\W_])", re.IGNORECASE)
    if ms_keyword.search(file_name) is not None or ms_start_keyword.match(file_name) is not None:
        return True
    else:
        return False


def is_item_attachment(num, file, eco, rev, root):
    if num in file:
        logging.debug("TRUE NUM:\t%s\tIN FILE:\t%s\tSEARCH REV:\t%s" % (num, file, rev))
        if eco in root and eco != "1":
            logging.debug("TRUE ECO:\t%s\tIN ROOT:\t%s\tSEARCH REV:\t%s" % (eco, root, rev))
            if not is_material_spec(file):
                logging.debug("TRUE is not MS:\t%s\tSEARCH REV:\t%s" % (file, rev))
                if not is_a_bom_redline(file):
                    logging.debug("TRUE is not BOM Redline:\t%s\tSEARCH REV:\t%s" % (file, rev))
                    if not find_multiple_revs_in_file_name(os.path.splitext(file)[0]):
                        logging.debug("TRUE no multiple revs in:\t%s" % file)
                        if return_rev_from_file_name(os.path.splitext(file)[0]) == filter_zeros_from_rev(rev):
                            logging.debug("TRUE return_rev_from_file_name:\t%s\t== rev:%s\t%s" %
                                          (file, rev, filter_zeros_from_rev(rev)))
                            logging.debug("is_item_attachment:\tnum: %s\tfile: %s\teco: %s\trev: %s\troot: %s" %
                                          (num, file, eco, rev, root))
                            return True
                        elif is_new_rev_folder(root) and return_rev_from_file_name(file) is None:
                            logging.debug("TRUE is_new_rev_folder:\t%s\t%s" % (root, file))
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def perform_copy(num, rev, eco, root, file, line, copy_destination_dir):
    src_file = os.path.join(root, file)
    src_file_name, src_file_extension = os.path.splitext(src_file)
    if src_file_extension == ".pdf":
        # right now I only want to get pdf files because that is the data we have
        # TODO pull the hardcode .pdf extension out of here and make it selectable
        new_file_name = create_new_part_name(line) + src_file_extension  # get a new name
        new_dst_file_name = os.path.join(copy_destination_dir, new_file_name)
        if not os.path.exists(new_dst_file_name):
            shutil.copy(src_file, new_dst_file_name)
            logging.info("%s\t%s\t%s\t%s" % (num, rev, eco, new_dst_file_name))
        else:
            ii = 1
            while True:
                new_name = os.path.join(create_new_part_name(line) + "(" + str(ii) + ")" + src_file_extension)
                new_name_path = os.path.join(copy_destination_dir, new_name)
                if not os.path.exists(new_name_path):
                    shutil.copy(src_file, new_name_path)
                    logging.info("%s\t%s\t%s\t%s" % (num, rev, eco, new_name_path))
                    break
                ii += 1


def test_run_for_copy(num, rev, eco, root, file, line, copy_destination_dir):
    src_file = os.path.join(root, file)
    src_file_name, src_file_extension = os.path.splitext(src_file)
    if src_file_extension == ".pdf":
        # right now I only want to get pdf files because that is the data we have
        # TODO pull the hardcode .pdf extension out of here and make it selectable
        new_file_name = create_new_part_name(line) + src_file_extension  # get a new name
        new_dst_file_name = os.path.join(copy_destination_dir, new_file_name)
        if not os.path.exists(new_dst_file_name):
            print("copy src:\t%s\tto:\t%s" % (src_file, new_dst_file_name))
            logging.info("copy src:\t%s\tto:\t%s" % (src_file, new_dst_file_name))
            logging.debug("Target:\t%s-%s\ton ECO:\t%s\tfrom:\t%s\tto:\t%s" % (num, rev, eco, src_file, new_file_name))
        else:
            ii = 1
            while True:
                new_name = os.path.join(create_new_part_name(line) + "(" + str(ii) + ")" + src_file_extension)
                new_name_path = os.path.join(copy_destination_dir, new_name)
                if not os.path.exists(new_name_path):
                    print("copy src:\t%s\tto:\t%s" % (src_file, new_name_path))
                    logging.info("copy src:\t%s\tto:\t%s" % (src_file, new_name_path))
                    logging.debug("Target:\t%s-%s\ton ECO:\t%s\tfrom:\t%s\tto:\t%s" %
                                  (num, rev, eco, src_file, new_name))
                    break
                ii += 1


# @do_cprofile
def search_and_copy_part_attachments(part_rev_eco_index, file_loc_index, copy_destination_dir, debug=False):

    with open(part_rev_eco_index, "r+") as rev_index:  # open the part_rev_eco_index file assuming it's formatted
        for line in rev_index:  # look through each line
            if len(line) > 0:
                num = split_rev_table_data(line)[0]
                rev = split_rev_table_data(line)[1]
                eco = split_rev_table_data(line)[2].rstrip('\n')
                with open(file_loc_index, newline='', encoding='utf-8') as file_index:
                    reader = csv.reader(file_index, delimiter='\t')
                    for row in reader:
                        root = row[0]
                        file = row[1]
                        if is_item_attachment(num, file, eco, rev, root):
                            if not debug:
                                perform_copy(num, rev, eco, root, file, line, copy_destination_dir)
                            else:
                                test_run_for_copy(num, rev, eco, root, file, line, copy_destination_dir)
                    else:
                        logging.debug("Part Attachment not found for:\t%s" % line.rstrip('\n'))
            else:  # line length == 0
                logging.info("Zero length line: (%s)" % line)
