class User:
    def __init__(self, uid, name, password, token):
        self.uid = uid
        self.token = token
        self.password = password
        self.name = name

    def to_dict(self):
        return self.__dict__