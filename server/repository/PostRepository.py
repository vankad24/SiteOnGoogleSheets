from server.data.DataSource import Sheet
from server.model.ApiException import ApiException

from server.model.Post import Post


class PostRepository:
    def __init__(self, sheet):
        self.posts: Sheet = sheet
        self.column_title = "A"
        self.column_content = "B"

    def get_column_titles(self):
        """ Получить колонку (массив) заголовков """
        return self.posts.get_column(self.column_title)

    def get_post_by_id(self, id):
        """ Получить пост по id """
        row = self.posts.get_row_by_id(id)
        if row is None:
            raise ApiException("Wrong post id")
        if len(row) < 1:
            raise ApiException("Title is empty")
        if len(row) >= 2:
            content = row[1]
        else:
            content = ""
        title = row[0]
        post = Post(id, title, content)
        return post

    def add_post(self, title: str, content=""):
        """ Добавление строки title, content в конец таблицы. Если title = "", вызывает ApiException """
        if not title:
            raise ApiException("The title should be specified")
        data = [[title, content]]
        new_id = self.posts.append(data)
        return new_id

    def change_post(self, post: Post):
        """ Обновление поста в таблице """
        self.posts.update_row(post.id, post.title, post.content)

    def delete_post_by_id(self, id):
        """ Удаление поста в таблице """
        self.posts.delete_row(id)
