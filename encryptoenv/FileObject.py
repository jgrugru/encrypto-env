from os import path, remove, stat, makedirs


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
        makedirs(path.dirname(self.filepath), exist_ok=True)
        try:
            with open(self.filepath, "a") as f:
                f.write("")
        except Exception:
            pass

    def delete_file(self, verbose_flag=False):
        if self.filepath_exists() and self.is_file():
            remove(self.filepath)
            if verbose_flag:
                print("Deleted " + self.filepath)
        else:
            print("The file could not be deleted because "
                  + self.filepath + " does not exist or it is a directory.")

    def append_data_to_file(self, data, verbose_flag=False):
        f = open(self.filepath, 'a')
        f.write(data)
        f.close()

    def get_contents_of_file(self):
        if not self.is_binary():
            data = self.get_contents_of_text_file()
        else:
            data = self.get_contents_binary_file()
        return data

    def get_contents_of_text_file(self):
        data = None
        with open(self.filepath, 'r') as my_file:
            data = my_file.read()
        return data

    def get_contents_binary_file(self):
        data = None
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

    def is_dir(self, verbose_flag=False):
        return path.isdir(self.filepath)

    def is_file(self, verbose_flage=False):
        return path.isfile(self.filepath)

    def __str__(self):
        return self.filepath
