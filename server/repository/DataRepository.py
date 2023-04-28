from server.data.DataSource import SpreadSheet
from server.model.ApiException import ApiException

import json
from server.model.Post import Post
from googleapiclient.errors import HttpError


class DataRepository:
    def __init__(self, spreadsheet):
        self.sheet = spreadsheet.open_sheet("Sheet1")
        # self.user_sheet = self.spreadsheet.open_sheet("UsersSheet")

    def change_title(self, id, new_title):
        if not new_title:
            raise ApiException("title is empty")
        data = [[new_title]]
        range = "A" + str(id)
        self.sheet.update(range, data)  # what is range

    def get_all_titles(self):
        response = self.sheet.get_data(ranges=["A2:A"])
        result = {"titles": []}
        for i in response:
            count = 1
            for j in i:
                if j:
                    result["titles"] += [{"id": count, "title": j[0]}]
                count += 1
        return result


def main():
    """
        Shows the basic usage of the Sheets API.
    """

    db = SpreadSheet()
    print(json.dumps(db.get_spreadsheet_info(["Sheet1!A5", "Sheet2!A3"], True), indent=4))

    sh1 = db.open_sheet("Sheet1")

    print(sh1.get_row_by_id(7))
    print(sh1.get_cell_by_id(7, "a"))
    print(sh1.get_column("c"))
    print(sh1.get_column("e"))

    sh1.add_row("hello", "hi")
    sh1.add_row("one more", "row")
    sh1.add_row(12, 24)

    p = Post(14, "test", "bug")
    p1 = Post(15, "empty", "row")

    sh1.change_row(p)
    sh1.change_row(p1)
    sh1.add_row("one more", "test")

    sh1.delete_row(10)


if __name__ == '__main__':
    main()
