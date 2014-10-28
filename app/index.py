import os


def create_path_index(locations, write_file):
    for path in locations:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                if len(files) > 0:
                    with open(write_file, "a") as my_file:
                        for file in files:
                            if not file == "Thumbs.db":
                                my_file.write(str("%s\t%s" % (os.path.normpath(root), file)) + "\n")
                    my_file.close()
        else:
            raise TypeError("Path Doesn't Exist")
