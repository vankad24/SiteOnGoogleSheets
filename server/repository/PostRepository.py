from server.data.DataSource import Sheet
from server.model.ApiException import ApiException

from server.model.Post import Post


class PostRepository:
    def __init__(self, sheet):
        self.posts: Sheet = sheet
        self.column_title = "A"
        self.column_content = "B"
        self.column_head = "C"
        self.head_len = 200

    def get_column_titles(self):
        """ Получить колонку (массив) заголовков """
        return self.posts.get_column(self.column_title)

    def get_column_heads(self):
        """ Получить колонку (массив) обрезанного основного текста """
        return self.posts.get_column(self.column_head)

    def get_post_by_id(self, id):
        """ Получить пост по id """
        row = self.posts.get_row_by_id(id)
        if row is None:
            raise ApiException("Wrong post id")

        title = row[0]
        content = row[1]
        author_id = int(row[3])
        post = Post(id, title, content, author_id)
        return post

    def add_post(self, author_id, title: str, content=""):
        """ Добавление строки title, content в конец таблицы. Если title = "", вызывает ApiException """
        if not title:
            raise ApiException("The title should be specified")
        data = [[title, content, content[:self.head_len], author_id]]
        new_id = self.posts.append(data)
        return new_id

    def check_ids(self, author_id, uid):
        if author_id != uid and uid != 1:
            raise ApiException("You are not the author")
    def change_post(self, post: Post, uid):
        """ Обновление поста в таблице """
        self.check_ids(post.author_id,uid)
        self.posts.update_row(post.id, post.title, post.content, post.content[:self.head_len])

    def delete_post_by_id(self, id, uid):
        """ Удаление поста в таблице """
        post = self.get_post_by_id(id)
        self.check_ids(post.author_id,uid)
        self.posts.delete_row(id)
