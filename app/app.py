
import os


path_var = ["//mks-bld-105/ECP_ARCHIVE/ECP-ECO 2010", "//mks-bld-105/ECP_ARCHIVE/ECP-ECO 2011",
            "//mks-bld-105/ECP_ARCHIVE/ECP-ECO 2012", "//mks-bld-105/ECP_ARCHIVE/ECP-ECO 2013",
            "//mks-bld-105/ECP_ARCHIVE/ECP-ECO 2014"]

def create_path_index(locations):
    for path in locations:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                if len(files) > 0:
                    with open("ECO_attachments.txt", "a") as my_file:
                        for file in files:
                            if not file == "Thumbs.db":
                                my_file.write(str("%s\t%s" % (os.path.normpath(root), file))+"\n")
                    my_file.close()
        else:
            raise TypeError("Path Doesn't Exist")
