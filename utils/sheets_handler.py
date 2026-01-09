import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

class SheetsHandler:
    def __init__(self, sheet_url=None):
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "service_account.json")
        # Use provided URL or fallback to environment variable
        self.sheet_url = sheet_url
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
                if self.sheet_url:
                    print(f"Opening Google Sheet by URL: {self.sheet_url}")
                    self.sheet = self.client.open_by_url(self.sheet_url).sheet1
                else:
                    print(f"Opening Google Sheet by Name: {self.sheet_name}")
                    self.sheet = self.client.open(self.sheet_name).sheet1
            except gspread.SpreadsheetNotFound:
                if self.sheet_url:
                    print(f"Error: Spreadsheet with URL '{self.sheet_url}' not found or not accessible.")
                else:
                    print(f"Error: Spreadsheet '{self.sheet_name}' not found.")
                return False
            return True
        except PermissionError:
            print("\n" + "!"*50)
            print("PERMISSION ERROR: The service account does not have access to this sheet.")
            try:
                import json
                with open(self.creds_file) as f:
                    email = json.load(f).get('client_email')
                    print(f"Please SHARE your Google Sheet with this email: {email}")
                    print("Give it 'Editor' permissions.")
            except:
                print("Please check your service_account.json and share the 'client_email' with your Google Sheet.")
            print("!"*50 + "\n")
            return False
        except Exception as e:
            import traceback
            print(f"Error connecting to Google Sheets: {e}")
            traceback.print_exc()
            return False

    def append_data(self, data):
        """
        Appends a row of data to the sheet.
        Expected data format: {'title': '', 'author': '', 'date': '', 'url': '', 'metadata': {'views': '', 'likes': ''}}
        """
        if not self.sheet:
            if not self.connect():
                return

        row = [
            data.get('title', ''),
            data.get('author', ''),
            data.get('date', ''),
            data.get('metadata', {}).get('views', '0'),
            data.get('metadata', {}).get('likes', '0'),
            data.get('url', '')
        ]

        try:
            self.sheet.append_row(row)
            print(f"Successfully appended data for {data.get('url')}")
        except Exception as e:
            print(f"Error appending data: {e}")

    def append_rows(self, data_list):
        """
        Appends multiple rows of data to the sheet in a single call.
        """
        if not self.sheet:
            if not self.connect():
                return

        rows = []
        for data in data_list:
            rows.append([
                data.get('title', ''),
                data.get('author', ''),
                data.get('date', ''),
                data.get('metadata', {}).get('views', '0'),
                data.get('metadata', {}).get('likes', '0'),
                data.get('url', '')
            ])

        try:
            self.sheet.append_rows(rows)
            print(f"Successfully appended {len(rows)} rows to Google Sheet.")
        except Exception as e:
            print(f"Error appending batch data: {e}")

    def ensure_header(self):
        """Ensures the sheet has the correct header row."""
        if not self.sheet:
             if not self.connect():
                return

        header = ["Title", "Author", "Date", "Views", "Likes", "URL"]
        try:
            existing_header = self.sheet.row_values(1)
            if not existing_header:
                self.sheet.append_row(header)
                print("Added header row to Google Sheet.")
        except Exception as e:
            print(f"Error checking/adding header: {e}")

    def clear_sheet(self):
        """Clears all content from the sheet."""
        if not self.sheet:
            if not self.connect():
                return
        try:
            self.sheet.clear()
            print("Successfully cleared the Google Sheet.")
        except Exception as e:
            print(f"Error clearing sheet: {e}")
