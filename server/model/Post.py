class Post:
    def __init__(self, pid, title, content):
        self.content = content
        self.title = title
        self.id = pid

    def to_dict(self):
        return self.__dict__