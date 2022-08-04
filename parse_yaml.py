import yaml


class ParseYaml(object):

    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, 'r', encoding='utf-8') as f:
            self.data = yaml.load(f, Loader=yaml.SafeLoader)
            # self.ip = self.data.get("ip")
            # self.port = self.data.get("port")
            # self.username = self.data.get("username")
            # self.password = self.data.get("password")
            f.close()

    def parse(self):
        return self.data


if __name__ == '__main__':
    parse = ParseYaml("auto.yaml")
    print(parse.parse())

