import os


def create_path_index(location, write_file):
        if os.path.exists(location):
            for root, dirs, files in os.walk(location):
                if len(files) > 0:
                    with open(write_file, "a") as my_file:
                        for file in files:
                            if not file == "Thumbs.db":
                                my_file.write(str("%s\t%s" % (os.path.normpath(root), file)) + "\n")
                    my_file.close()
        else:
            raise TypeError("Path Doesn't Exist")
