from utils.config_utils import load_config
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import json
import os

config = load_config()
credentials_file = config['google']['sheets']['credentials_file']
spreadsheet_id = config['google']['sheets']['spreadsheet_id']

def get_sheet_id(service , sheet_name):
    # Get the spreadsheet metadata
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])

    # Find the sheet ID for the given sheet name
    for sheet in sheets:
        if sheet.get("properties", {}).get("title") == sheet_name:
            return sheet.get("properties", {}).get("sheetId")
    return None

def headers_exist(service, sheet_name):
    # Check if headers already exist in the Google Sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!A1:F1'
    ).execute()
    
    headers = result.get('values', [])
    if headers:
        existing_headers = headers[0]
        required_headers = ["Date", "Reference URL", "Hook", "Build Up", "Body", "CTA"]
        return set(existing_headers) >= set(required_headers)
    return False

def store_in_google_sheets(transcriptions):
    creds = Credentials.from_service_account_file(credentials_file)
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    # Check if headers already exist
    if headers_exist(service, 'Sheet1') == False:
        # Add headers if they don't exist
        print("Adding headers to the sheet")
        transcriptions.insert(0, ["Date", "Reference URL", "Hook", "Build Up", "Body", "CTA"])

    # Append the transcriptions to the sheet
    body = {
        'values': transcriptions
    }
    result = sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f"{result.get('updates').get('updatedCells')} cells updated.")

    # Get the sheet ID
    sheet_id = get_sheet_id(service, "Sheet1")
    if sheet_id is None:
        print("Sheet1 not found")
        return

    # Formatting requests
    requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "startColumnIndex": 0,
                    "endColumnIndex": len(transcriptions[0])
                },
                "cell": {
                    "userEnteredFormat": {
                        "wrapStrategy": "WRAP",
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(wrapStrategy,horizontalAlignment,verticalAlignment)"
            }
        }
    ]

    # Apply formatting
    body = {
        'requests': requests
    }
    response = sheet.batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    print(f"{response}")

if __name__ == "__main__":
    
    pre_processed_path = config["paths"]["preprocessed_videos"]   
    transcriptions = []

    # Iterate through JSON files in the preprocessed folder
    for file_name in os.listdir(pre_processed_path):
        if file_name.endswith(".json"):
            with open(os.path.join(pre_processed_path, file_name), "r") as f:
                data = json.load(f)
                transcription = [
                    data.get("date", ""),
                    data.get("Reference URL", ""),
                    data.get("Hook", ""),
                    data.get("Build Up", ""),
                    data.get("body", ""),
                    data.get("CTA", "")
                ]
                transcriptions.append(transcription)

    store_in_google_sheets(transcriptions)
