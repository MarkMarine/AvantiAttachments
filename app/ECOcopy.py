import os.path, shutil, logging

location = "c:\\avanti"
dest_location = "h:\\avanti\\eco_attachments\\"

try:
    for dirpath, dirnames, filenames in os.walk(location):
    # Go through the directory list, and dig down two levels (root, first sub folder) then copy
    # the ECO folder out (removing the name ECO or spaces) to the H:\avanti\eco_attachments location
        lst = (os.path.normpath(dirpath).split("\\"))  # Split the file names on a \ to count the dirs
        if len(lst) == 4:  # Dig to the ECO level and copy those directories only
            if not os.path.exists("%s%s" % (dest_location, lst[3])):
                shutil.copytree(dirpath, "%s%s" % (dest_location, lst[3]))

except OSError:
    print("error")