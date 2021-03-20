from os import path


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

    def delete_file(self):
        pass

    def get_contents_of_file(self):
        with open(self.filepath, 'r') as my_file:
            data = my_file.read()

        return data

    def __str__(self):
        return self.filepath

