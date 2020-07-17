from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GSheetsAppender:
    def __init__(self, spreadsheet_id, range, creds):
        self.spreadsheet_id = spreadsheet_id
        self.range = range
        self.creds = creds


    def append(self, data):
        service = build('sheets', 'v4', credentials=self.creds)
        sheet = service.spreadsheets()

        resource = {
            "majorDimension": "ROWS",
            "values": data
        }

        request = sheet.values().append(
            spreadsheetId=self.spreadsheet_id,
            range=self.range,
            valueInputOption="USER_ENTERED",
            body=resource
        )

        response = request.execute()

        print(response)



def test():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets'
    ]

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1bSv_dV32-QspYtcfYvaby82UGy4PsnBoXg9lvCsKie4'
    SAMPLE_RANGE_NAME = 'Sheet1!A1:D1'

    pathToFile = os.path.join(os.getcwd(), "_secrets", 'krakow-house-prices-1fb495b73c88.json')
    creds = service_account.Credentials.from_service_account_file(
        pathToFile, scopes = SCOPES
    )

    rows = [
        ["Door", "$15", "2", "3/15/2016"],
        ["Engine", "$100", "1", "3/20/2016"],
    ]

    appender = GSheetsAppender(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, creds)
    appender.append(rows)


if __name__ == '__main__':
    test()

