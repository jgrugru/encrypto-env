from os import path, remove


class FileObject():

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_filepath(self):
        return self.filepath

    def filepath_exists(self):
        if path.isdir(self.filepath) or path.exists(self.filepath):
            return True
        else:
            return False

    # def create_filepath(self):
    #     pass

    def delete_file(self, verbose_flag=False):
        if self.filepath_exists():
            if verbose_flag:
                print("Removing " + self.filepath)
            remove(self.filepath)

    def get_contents_of_file(self, is_encrypted=False):
        if not is_encrypted:
            with open(self.filepath, 'r') as my_file:
                data = my_file.read()
        else:
            with open(self.filepath, 'rb') as my_file:
                data = my_file.read()     
        return data

    def __str__(self):
        return self.filepath

