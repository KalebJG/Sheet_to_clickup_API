pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client clickuppy

import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from clickuppy import ClickUp

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = 'YOUR_GOOGLE_SPREADSHEET_ID'
RANGE_NAME = 'Sheet1!A:D'  # Update with the appropriate sheet and range

# ClickUp API setup
CLICKUP_API_KEY = 'YOUR_CLICKUP_API_KEY'
CLICKUP_SPACE_ID = 'YOUR_CLICKUP_SPACE_ID'
CLICKUP_FOLDER_ID = 'YOUR_CLICKUP_FOLDER_ID'
CLICKUP_LIST_ID = 'YOUR_CLICKUP_LIST_ID'

def read_google_sheet():
    credentials = service_account.Credentials.from_service_account_file('path/to/your/credentials.json', scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    return values

def create_clickup_task(task_data):
    clickup = ClickUp(CLICKUP_API_KEY)

    task_data = {
        'name': task_data[0],
        'description': task_data[1],
        'status': 'Open',  # Update with your desired status
        'priority': 2,  # Update with your desired priority
    }

    task = clickup.task.create_task(
        list_id=CLICKUP_LIST_ID,
        name=task_data['name'],
        content=task_data['description'],
        status=task_data['status'],
        priority=task_data['priority']
    )

    print(f'Created ClickUp task: {task["name"]}')

if __name__ == '__main__':
    last_row_count = 0

    while True:
        sheet_data = read_google_sheet()
        current_row_count = len(sheet_data)

        if current_row_count > last_row_count:
            new_rows = sheet_data[last_row_count:]
            for row in new_rows:
                create_clickup_task(row)

            last_row_count = current_row_count

        time.sleep(60)  # Check for changes every 60 seconds
