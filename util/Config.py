class Config:

    def __init__(self, path='config'):
        self.path = path
        self.config = {}
        self.selected = None
        self.parse_config(path)

    def parse_config(self, path):
        file = open(path, "r").read()
        for line in file.splitlines():
            key = line.split(' ')[0]
            value = (line.split(' ')[1], int(line.split(' ')[2]))
            self.config[key] = value

    def get(self, type):
        self.selected = self.config[type.value]
        return self

    def get_port(self) -> str:
        return self.selected[1]

    def get_group(self) -> int:
        return self.selected[0]

    def get_info(self) -> tuple:
        ip, port = self.selected
        return ip, port
