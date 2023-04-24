from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Secrets:

    SAMPLE_SPREADSHEET_ID = '1ZpkI-J3CUBtHpJqit1dLrPppIW8cUWvGcPeRVtd0PH4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


    def __int__(self, token_file, creds_file):

        """ token_file = the file the token will be saved into, creds_file is the same but for credentials """

        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        self.credentials = creds


    def get_credentials(self):
        return self.credentials


    def get_spreadsheetid(self):
        return self.SAMPLE_SPREADSHEET_ID




class SpreadSheet():

    def __init__(self, credentials, spreadsheet_id):
        secrets = Secrets() #todo insert files
        self.credentials = secrets.get_credentials()
        self.spreadsheet_id =  secrets.get_spreadsheetid()
        self.spreadsheet = build('sheets', 'v4', credentials=credentials).spreadsheets()


    def get_sheets_list(self, ranges=None, include_grid_data=None):
        return self.spreadsheet.get(spreadsheetId=self.spreadsheet_id, ranges=ranges, includeGridData =include_grid_data).execute()


    def open_sheet(self, name):
        return Sheet(self, name)



class Sheet():

    def __init__(self, inst, name):
        self.__dict__ = dict(inst.__dict__)
        self.name = name
        self.values = self.spreadsheet.values()


    def get_data(self, ranges : list):
        """
            get data with the given ranges, where the ranges obejct is a list of lists
        """
        ranges1 = []
        for i in ranges:
             ranges1 += [self.name + "!" + i]

        try:

            response = self.values.batchGet(spreadsheetId=self.spreadsheet_id, ranges=ranges1).execute()["valueRanges"]
        except HttpError as error:
            print(error)


        result = ()
        for i in response:
            if "values" in i:
                result += (i["values"], )
            else:
                result += (None, )
        return result


    def append(self, data : list, majorDimension="ROWS"):
        """data is a list of lists. Returns None if error occured"""
        body = {
            "range": self.name,
            "majorDimension": majorDimension,
            "values": data
        }
        try:

            self.spreadsheet.values().append(spreadsheetId=self.spreadsheet_id, range=self.name, valueInputOption = "USER_ENTERED", body=body).execute()
            return response
        except HttpError as error:
            print(error)
            return None


    def update(self, data, range : list, majorDimension="ROWS"):

        """ updates the given range, data is a list of lists. Returns None if error occured"""

        body = {
                "majorDimension": majorDimension,
                "values": data
        }
        try:
            response = self.values.update(spreadsheetId=self.spreadsheet_id, range=self.name + "!" + range, valueInputOption="USER_ENTERED", body=body).execute()
            return response
        except HttpError as error:
            print(error)
            return None


    # def get(self, id : int):
    #     row = str(id)
    #     return self.get_data([row + ":" + row])


    # def get_all_titles(self):
    #     response = self.get_data(ranges=["A2:A"])
    #     result = {"titles":[]}
    #     for i in response:
    #         count = 1
    #         for j in i:
    #             if j != []:
    #                 result["titles"] += [{"id": count, "title" : j[0]}]
    #             count += 1
    #     return result


    # def add(self, title, content=""):
    #     data = [[title, content]]
    #     try:
    #         response = self.append(data)
    #         return {"status" : True}
    #     except HttpError as error:
    #         return {"status" : False, "error" : error}


    # def change_title(self, id, new_title):
    #     try:
    #         data = [[new_title]]
    #         print(self.name + "!A" + str(id))
    #         body = {
    #             "majorDimension": "ROWS",
    #             "values": data
    #         }
    #         self.values.update(spreadsheetId=self.spreadsheet_id, range=self.name + "!A" + str(id), valueInputOption="USER_ENTERED", body=body).execute()
    #         return {"status" : True}
    #     except HttpError as error:
    #         return {"status" : False, "error" : error}


    def read(self):
        print(f"Will read sheet {self.name} using credentials {self.credentials}")
