from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient
from googleapiclient.discovery import Resource, build
from googleapiclient.http import MediaFileUpload

import pandas as pd
import os

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

class GoogleSheets:
    sheets_service: Resource
    drive_service: Resource
    def __init__(self):
        self.sheets_service, self.drive_service = self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return build('sheets', 'v4', credentials=creds), build('drive', 'v3', credentials=creds)        

    # You can now add other methods to interact with Google Sheets API using self.service


    
    def upload_csv(self, csv_path, sheet_title):
        """
        Uploads a CSV file to Google Sheets.

        Args:
            csv_path (str): Path to the CSV file.
            sheet_title (str): Desired title for the new Google Sheet.
        
        Returns:
            str: URL of the created Google Sheet.
        """      
        # Metadata for the new Google Sheet file
        file_metadata = {
            'name': sheet_title,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }

        media = MediaFileUpload(csv_path, mimetype='text/csv', resumable=True)
        
        # Upload the CSV and convert to Google Sheets
        file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='webViewLink').execute()
        
        return file.get('webViewLink')

    def list_files(self):
        files = self.drive_service.files().list().execute()
        for file in files['files']:
            if file['name'] == 'Hotel Partner Pipeline':
                print (file['name'])
        print(files)
        return files

    def download_sheet_data(self, file_id):
        """
        Downloads data from a specific range of a Google Sheet.

        Args:
            spreadsheet_id (str): The ID of the Google Sheet.
            data_range (str): The range of cells to download, in the format 'SheetName!A1:Z100'.

        Returns:
            list: 2D list representing the rows and columns of the downloaded data.
        """
        file = self.sheets_service.spreadsheets().get(spreadsheetId = file_id).execute()
        range_name = "A1:Z"  # Assuming a maximum of 26 columns, adjust if necessary

        result = self.sheets_service.spreadsheets().values().get(spreadsheetId=file_id, range=range_name).execute()
        values = result.get('values', [])
        headers = values[0]  # First row is the header
        data_dicts = []

        if not values:
            print('No data found.')
            return []

        for row in values[1:]:
            data_dict = {headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))}
            data_dicts.append(data_dict)

        hotel_set = {row['Hotel'] for row in data_dicts if 'Hotel' in row and row['Hotel'] is not None}

        return hotel_set


if __name__ == '__main__':
    secrets_path = 'google_secret.json'
    sheets = GoogleSheets()
    # f = sheets.list_files()
    # url = sheets.upload_csv('arizona.csv', 'Test Upload')
    file_id = '1g9zwbC3w0ROna5k5ybOJtlV2SY_4b4RC-pHDeQSvyT8'
    df = sheets.download_sheet_data(file_id)
    print(df)