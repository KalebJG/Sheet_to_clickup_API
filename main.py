import os
import time
from googleapiclient.discovery import build
from clickuppy import ClickUp

# Google Sheets API setup
SPREADSHEET_ID = 'Google Sheet ID'
RANGE_NAME = 'Sheet1!A:D'  # Update with the appropriate sheet and range
API_KEY = 'Google API Key'

# ClickUp API setup
CLICKUP_API_KEY = 'API Key'
CLICKUP_SPACE_ID = 'Space ID'
CLICKUP_FOLDER_ID = 'Folder ID'
CLICKUP_LIST_ID = 'List ID'

def read_google_sheet():
    service = build('sheets', 'v4', developerKey=API_KEY)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    return values

def create_clickup_task(task_data):
    clickup = ClickUp(CLICKUP_API_KEY)

    task_data = {
        'name': task_data[3],
        'assignment id': task_data[2],
        'department': task_data[1],
        'status': 'Open',  # Update with your desired status
        'priority': 2,  # Update with your desired priority
    }

    task = clickup.task.create_task(
        list_id=CLICKUP_LIST_ID,
        name=task_data['name'],
        content=task_data['assignment id'],
        status=task_data['status'],
        priority=task_data['priority'],
        custom_fields={
            'department': task_data['department'],
        }
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

