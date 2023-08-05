class Tee:
    def __init__(self, name, f):
        self.file = open(name, "w")
        self.name = name
        self.original = f

    def close(self):
        if hasattr(self, "file"):
            if self.file is not None:
                # noinspection PyUnresolvedReferences
                self.file.close()
                self.file = None

    def __del__(self):
        self.close()

    def write(self, data: str):
        # if isinstance(data, str):
        #     data = data.encode('utf-8')
        self.file.write(data)
        self.file.flush()
        # data_s = data.decode('utf-8')
        self.original.write(data)
        self.original.flush()

    def flush(self):
        self.file.flush()
        self.original.flush()

    def fileno(self):
        return self.file.fileno()

    def getvalue(self):
        with open(self.name) as f:
            return f.read()
