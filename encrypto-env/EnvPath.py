from os import path, mkdir, getcwd


class EnvPath():

    default_path = getcwd() + '/env'

    def __init__(self, env_path=default_path):
        self.env_path = env_path

    def set_env_path(self, folder_path):
        self.env_path = folder_path

    def get_env_path(self):
        return self.env_path

    def env_path_exists(self):
        if path.isdir(self.env_path):
            return True
        else:
            return False

    def create_env_path(self):
        if self.env_path_exists():
            print(self.env_path + " already exists.")
        else:
            try:
                mkdir(self.env_path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s " % path)
