class Post:
    def __init__(self, pid, title, content, author_id):
        self.author_id = author_id
        self.content = content
        self.title = title
        self.id = pid

    def to_dict(self):
        return self.__dict__