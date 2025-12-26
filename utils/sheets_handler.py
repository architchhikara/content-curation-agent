import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

class SheetsHandler:
    def __init__(self):
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "service_account.json")
        self.sheet_name = os.getenv("GOOGLE_SHEET_NAME", "ContentData")
        self.client = None
        self.sheet = None

    def connect(self):
        """Authenticates with Google Sheets API."""
        if not os.path.exists(self.creds_file):
            print(f"Error: {self.creds_file} not found. Cannot connect to Google Sheets.")
            return False

        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_file, self.scope)
            self.client = gspread.authorize(creds)
            # Open the spreadsheet
            try:
                self.sheet = self.client.open(self.sheet_name).sheet1
            except gspread.SpreadsheetNotFound:
                print(f"Error: Spreadsheet '{self.sheet_name}' not found.")
                return False
            return True
        except Exception as e:
            print(f"Error connecting to Google Sheets: {e}")
            return False

    def append_data(self, data):
        """
        Appends a row of data to the sheet.
        Expected data format: {'source': '', 'author': '', 'date': '', 'text': '', 'url': ''}
        """
        if not self.sheet:
            if not self.connect():
                return

        row = [
            data.get('source', ''),
            data.get('author', ''),
            data.get('date', ''),
            data.get('text', ''),
            data.get('url', '')
        ]

        try:
            self.sheet.append_row(row)
            print(f"Successfully appended data for {data.get('url')}")
        except Exception as e:
            print(f"Error appending data: {e}")

    def ensure_header(self):
        """Ensures the sheet has the correct header row."""
        if not self.sheet:
             if not self.connect():
                return

        header = ["Source", "Author", "Date", "Text/Transcript", "URL"]
        try:
            existing_header = self.sheet.row_values(1)
            if not existing_header:
                self.sheet.append_row(header)
                print("Added header row to Google Sheet.")
        except Exception as e:
            print(f"Error checking/adding header: {e}")
