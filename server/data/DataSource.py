from os.path import join, dirname, abspath, exists

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from server.model.ApiException import ApiException


class Secrets:

    SAMPLE_SPREADSHEET_ID = '1ZpkI-J3CUBtHpJqit1dLrPppIW8cUWvGcPeRVtd0PH4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    basepath = dirname(__file__)
    TOKEN_FILE = abspath(join(basepath, "..", "token.json"))
    CREDENTIALS_FILE = abspath(join(basepath, "..", "credentials.json"))

    def __init__(self):

        """
            token_file - файл, в который будет сохранен токен (либо токен будет взят из этого файла, если файл существует)
            creds_file - файл с секретными ключами (необходимо иметь его по умолчанию (получить его можно в google cloud console)
        """

        creds = None

        if exists(self.TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            # with open(self.TOKEN_FILE, 'w') as token:
            #     token.write(creds.to_json())

        self.credentials = creds

    def get_credentials(self):
        """ Поучить секретные ключи """
        return self.credentials

    def get_spreadsheetid(self):
        """ Получить id google sheet документа """
        return self.SAMPLE_SPREADSHEET_ID


class SpreadSheet:
    """ Класс для взаимодействия с google sheet документом """

    def __init__(self):
        secrets = Secrets()
        self.credentials = secrets.get_credentials()
        self.spreadsheet_id = secrets.get_spreadsheetid()
        self.spreadsheet = build('sheets', 'v4', credentials=self.credentials).spreadsheets()

    def get_spreadsheet_info(self, ranges=None, include_grid_data=None):
        """
            Получение полной информации по всему файлу google sheets
            range - получение данных по диапазону (использовать A1 нотацию (см в документации api google sheets))
            range сработает, только если include_grid_data=True, иначе - HttpError
        """
        return self.spreadsheet.get(spreadsheetId=self.spreadsheet_id, ranges=ranges, includeGridData=include_grid_data).execute()

    def open_sheet(self, name):
        """
            Создать объект класса Sheet с определенным названием,
            причем sheet с этим название уже должен существовать в google sheets документе
        """
        return Sheet(self, name)


class Sheet:

    """ Класс для взаимодействия с листом в google sheets документе"""

    def __init__(self, inst: SpreadSheet, name):
        self.credentials = inst.credentials
        self.spreadsheet_id = inst.spreadsheet_id
        self.spreadsheet = inst.spreadsheet
        self.name = name
        self.values = self.spreadsheet.values()

    def __check_list(self, list1):
        if not(list1 and all(i for i in list1)):
            raise ApiException("The list shouldn't be empty and the internal lists too")

    def __get_data(self, ranges: list):
        """
            Получить данные в пределах нескольких диапазонов (ranges). ranges = 2D array.
            Каждый диапазон записывается в A1 нотации (см в документации api google sheets)
            Вызывает ApiException, если ranges имеет неверный формат, и HttpError, если возникла ошибка на стороне google sheets api
            Возвращаете ответ в таком виде: (range1_values, range2_values), где range1_values = 2D array
        """

        # исключает подобные случаи: [], [[]], [["a"], []]
        self.__check_list(ranges)

        ranges1 = []
        for i in ranges:
            if not isinstance(i[0], str):
                raise ApiException("The range should be string")
            ranges1 += [self.name + "!" + i[0]]

        response = self.values.batchGet(spreadsheetId=self.spreadsheet_id, ranges=ranges1).execute()["valueRanges"]

        result = ()
        for i in response:
            if "values" in i:
                result += (i["values"], )
            else:
                result += (None, )
        return result

    def __update(self, data: list, range: str, majorDimension="ROWS"):

        """
            Обновляет заданный диапазон
            Диапазон записывается в A1 нотации (см в документации api google sheets)
            data = новые данные, представляет собой 2D array
            Если есть ошибка в параметрах функции, вызывает ApiException
            Возвращает статус операции и доп данные. Если возникает ошибка, вызывает HttpError
        """

        self.__check_list(range)

        body = {
                "majorDimension": majorDimension,
                "values": data
        }
        response = self.values.update(spreadsheetId=self.spreadsheet_id, range=self.name + "!" + range, valueInputOption="USER_ENTERED", body=body).execute()
        return response

    def __clear(self, range: str):

        """
            Удаляет данные в заданном диапазоне range
            range = string. Вызывает ApiException, если range = ""
            Возвращает статус операции и доп информацию. Если возникает ошибка, вызывает HttpError
        """

        if range == "":
            raise ApiException("The range should be specified")

        body = {}   # must be empty

        response = self.values.clear(spreadsheetId=self.spreadsheet_id, range=self.name + "!" + range, body=body).execute()
        return response

    def append(self, data: list, majorDimension="ROWS"):
        """
            Добавляет строку (data) в конец листа
            data = 2D array
            majorDimensions = не трогать
            Возвращает статус операции и доп информацию. Если возникает ошибка, вызывает HttpError
        """

        body = {
            "range": self.name,
            "majorDimension": majorDimension,
            "values": data
        }

        response = self.spreadsheet.values().append(spreadsheetId=self.spreadsheet_id, range=self.name, valueInputOption="USER_ENTERED", body=body).execute()
        updated_cell = response['updates']['updatedRange'].split(":")[-1]
        start = 0
        while not updated_cell[start].isdigit():
            start+=1
        new_id = int(updated_cell[start:])
        return new_id

    def get_row_by_id(self, id: int):
        """ Получение данных по строке, имеющей порядковый номер = id. None, если строка пуста"""
        row = str(id)
        response = self.__get_data([[row + ":" + row]])[0]
        if response is None:
            return None
        return response[0]

    def get_cell_by_id(self, id: int, column: str):
        """ Получение ячейки по ее порядковому номеру и названию столбца. None, если ячейка пуста """
        row = str(id)
        response = self.__get_data([[column.upper() + row]])[0]
        if response is None:
            return None
        return response[0][0]

    def get_column(self, column: str):
        """ Получение данных в столбце по его названию. None, если столбец пуст. Пустые ячейки заполнит None """
        col = column.upper()
        data = self.__get_data([[col + ":" + col]])[0]
        if data is None:
            return [None]
        return list(map(lambda x: x[0] if x else None, data))

    def update_row(self, id, *row):
        """Обновление строки в таблице """
        data = [row]
        id = str(id)
        response = self.__update(data, id + ":" + id)
        # return response

    def delete_row(self, id):
        """ Удаление строки в таблице по ее порядковому номеру """
        id1 = str(id)
        response = self.__clear(id1 + ":" + id1)
        # return response

def main():
    """ Shows the basic usage of the Sheets API. """

    db = SpreadSheet()
    # print(json.dumps(db.get_spreadsheet_info(["Sheet1!A5", "Sheet2!A3"], True), indent=4))

    sh1 = db.open_sheet("Sheet1")

    print(sh1.get_cell_by_id(7, "a"))
    print(sh1.get_column("a"))
    print(sh1.get_column("b"))
    print(sh1.get_row_by_id(7))
    print(sh1.append([["hi",25]]))
    # sh1.delete_row(7)
    # print(sh1.get_row_by_id(7))

    # sh1.add_row("hello", "hi")
    # sh1.add_row("one more", "row")
    # sh1.add_row(12, 24)
    # p = Post(14, "test", "bug")
    # p1 = Post(15, "empty", "row")

    # sh1.change_row(p)
    # sh1.change_row(p1)
    # sh1.add_row("one more", "test")

if __name__ == '__main__':
    main()