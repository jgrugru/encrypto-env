from os import path, mkdir, getcwd, remove


class FileObject():

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_filepath(self):
        return self.filepath

    def filepath_exists(self):
        if path.isdir(self.filepath):
            return True
        else:
            return False

    # def create_filepath(self):
    #     pass

    def delete_file(self):
        pass
    
    def __str__(self):
        return self.filepath