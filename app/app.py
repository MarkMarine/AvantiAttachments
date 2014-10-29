
# region Description of Functions
# Load both text files into memory

# Save a doc for loading into the item attachments for each revision:
# Line by line of the rev table, search the attachments for the appropriate part number + rev match. Get the new rev
# value from the REV Table (3 digit Rev) and attempt to match the part number + new rev combo.
# If new rev == true:
# Once you've selected the proper attachment file name, re-name the file to be <PARTNUMBER>-REV<###>.<ext> and
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

def main():
    # part_rev_eco_index = os.path.normpath(input("What is the location of the Part-REV-ECO index? "))
    # # TODO remove this second input, this program should create this on it's own in normal use
    # file_loc_index = os.path.normpath(input("What is the location of the file_location_index? "))
    # copy_destination_dir = os.path.normpath(input("What is the location should the files be copied to? "))
    debug_level = input("What should the debug level be: DEBUG, INFO, WARNING, ERROR? ")
    part_rev_eco_index = os.path.normpath(
        "c:/users/foxma/documents/github/avantiattachments/indexes/ItemNewRevW_O_sftwr.txt")
    file_loc_index = os.path.normpath("c:/users/foxma/documents/github/avantiattachments/indexes/local_att_delim.txt")
    copy_destination_dir = os.path.normpath("c:/users/foxma/documents/github/avantiattachments/results")
    debug = False
    if debug_level == "DEBUG":
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)
        debug = True
    elif debug_level == "INFO":
        logging.basicConfig(filename='info.log', level=logging.INFO)
    elif debug_level == "WARNING":
        logging.basicConfig(filename='warning.log', level=logging.WARNING)
    elif debug_level == "ERROR":
        logging.basicConfig(filename='error.log', level=logging.ERROR)
    else:
        logging.basicConfig(filename='error.log', level=logging.ERROR)

    search.search_and_copy_part_attachments(part_rev_eco_index, file_loc_index, copy_destination_dir, debug)


if __name__ == "__main__":
    import logging
    import os
    import search
    main()
