import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsClient:
    """
    Gets data from Google Sheets. Specifically, the guild's command channels and the bot's custom responses.
    """

    music_services_column = 5

    def __init__(self):
        print("Connecting to Google Sheets...")
        self.refresh_records()

    def refresh_records(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("./secret/google_sheets_secret.json", scope)
        client = gspread.authorize(credentials)
        master_sheet = client.open("Discord Assistant Bot")

        self.permissions_sheet = master_sheet.worksheet("Permissions")
        self.custom_response_sheet = master_sheet.worksheet("Custom Responses")
        self.permissions = None
        self.custom_response_records = None

        self.permissions = self.permissions_sheet.get_all_records()
        self.custom_response_records = self.custom_response_sheet.get_all_records()

    def get_command_channel_id(self, server_id):
        for entry in self.permissions:
            if str(entry["server_id"]) == server_id:
                return entry["command_channel_id"]

    def get_supported_audio_sites(self):
        return self.permissions_sheet.col_values(self.music_services_column)

    def get_custom_response(self, text):
        for entry in self.custom_response_records:
            trigger_phrases = str(entry["trigger_phrases"]).split(', ')

            for phrase in trigger_phrases:
                if phrase in text:
                    return entry["response"]

    def is_command_channel(self, text_channel, server_id):
        for entry in self.permissions:
            if str(entry["server_id"]) == server_id and entry["command_channel_name"] == text_channel:
                return True

        return False
