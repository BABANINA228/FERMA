from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class LoginData:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    accs_with_prime = 5
    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1c2ASZRPstVLCLXPyn8aNV_jrcFflRIZ03oqDo4RzNoE'

    @classmethod
    def get_login_data(cls, acc_ids):
        for i in range(len(acc_ids)):
            acc_ids[i] += 2

        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', cls.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', cls.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        for i in range(len(acc_ids)):
            acc_id = acc_ids[i]
            try:
                service = build('sheets', 'v4', credentials=creds)

                # Call the Sheets API B4:J4
                sheet = service.spreadsheets()
                result = sheet.values().get(spreadsheetId=cls.SPREADSHEET_ID,
                                            range=f'list 1!B{acc_id}:J{acc_id}').execute()
                values = result.get('values', [])

                if not values:
                    print('No data found.')
                    return

                for row in values:
                    # Print columns A and E, which correspond to indices 0 and 4.
                    print('%s %s' % (row[0], row[3]))
            except HttpError as err:
                print(err)


LoginData.get_login_data([1, 2, 5])
