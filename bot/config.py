import json


class BotConfig(object):
    def load(self, **kwargs):
        raise NotImplementedError


class FileBotConfig(BotConfig):
    """ Loads config from json file """
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path) as config_file:
            data = json.load(config_file)
            return data


if __name__ == "__main__":
    print(FileBotConfig('../config.json').load())