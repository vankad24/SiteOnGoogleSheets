from server.data.DataSource import Sheet
from server.model.ApiException import ApiException
from server.model.User import User


class UserRepository:
    def __init__(self, sheet):
        self.users: Sheet = sheet
        self.column_name = "A"
        self.column_password = "B"
        self.column_token = "C"


    def login(self, name, password):
        if not name or not password:
            raise ApiException("Incorrect request")
        names = self.users.get_column(self.column_name)
        if name not in names:
            raise ApiException(f"The nickname '{name}' is not registered")
        else:
            index = names.index(name)+1
            row = self.users.get_row_by_id(index)
            if row[1] != password:
                raise ApiException("Wrong password")
            else:
                user = User(index, row[0], row[1], row[2])
                return user

    def get_user_by_token(self, token):
        tokens = self.users.get_column(self.column_token)
        if not token or token not in tokens:
            raise ApiException("Invalid token")
        index = tokens.index(token) + 1
        row = self.users.get_row_by_id(index)
        user = User(index, row[0], row[1], row[2])
        return user

    def get_user_by_id(self, id):
        id = int(id)
        row = self.users.get_row_by_id(id)
        if row is None:
            raise ApiException("Wrong id")
        user = User(id, row[0], row[1], row[2])
        return user
