from os import path, remove, stat


class FileObject():
    """
    Base file class inherited by EnvDir, EnvFile,
    PemFile. Contains functions that can be utilized by any file.
    IS_BINARY() and IS_EMPTY() are largely useful during testing.
    """
 
    def __init__(self, filepath):
        self.filepath = filepath

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_filepath(self):
        return self.filepath

    def filepath_exists(self):
        if path.isdir(self.filepath) or path.exists(self.filepath):
            return True
        else:
            return False

    def create_filepath(self, verbose_flag=False):
        if not path.exists(self.filepath):
            open(self.filepath, 'a').close()
            if verbose_flag:
                print("Created blank file at " + self.filepath)

    def delete_file(self, verbose_flag=False):
        if self.filepath_exists():
            remove(self.filepath)
            if verbose_flag:
                print("Deleted " + self.filepath)
        else:
            print("The file could not be deleted because "
                  + self.filepath + " does not exist.")

    def get_contents_of_file(self):
        if not self.is_binary():
            with open(self.filepath, 'r') as my_file:
                data = my_file.read()
        else:
            with open(self.filepath, 'rb') as my_file:
                data = my_file.read()
        return data

    def clear_file(self, verbose_flag=False):
        if self.filepath_exists():
            open(self.filepath, 'w').close()
            if verbose_flag:
                print("Cleared the contents of " + self.filepath)
        else:
            print("The file could not be cleared because "
                  + self.filepath + " does not exist.")

    def is_binary(self, verbose_flag=False):
        try:
            with open(self.filepath, "r") as f:
                f.read()
        except UnicodeDecodeError:
            return True
        return False

    def is_empty(self, verbose_flag=False):
        if stat(self.filepath).st_size == 0:
            return True
        else:
            return False

    def __str__(self):
        return self.filepath
