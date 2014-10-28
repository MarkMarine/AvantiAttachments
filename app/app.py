import logging


logging.basicConfig(filename='debug.log', level=logging.DEBUG)
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
    pass


if __name__ == "__main__":
    main()
