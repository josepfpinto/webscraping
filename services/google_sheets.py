import os
from cProfile import label

from pathlib import Path
import config.sheets_id as sheet
from gspread import Spreadsheet, Worksheet
from selenium.common.exceptions import TimeoutException
import gspread
from google.oauth2 import service_account

from services import exceptions

wks = Worksheet
wksInput = Worksheet
sh = Spreadsheet


# --- Connects to Google Sheets and prepares sheets ---
def init(day):
    global wks, wksInput
    connect_to_google()

    # Prepare Google Sheets
    print("\nPreparing Google Sheets")
    print()
    if wks.acell("A1").value != "PLATF":
        print("- wrong set up in sheet!")
        wks.clear()
        wks.append_row(["PLATF", "TODAY", "DATE", "NAME", "RESERV", "SCORE", "PRICES"])
    elif len(wks.col_values(1)) == 1:
        print("- sheet empty")
    elif wks.row_values(2)[1] == day:
        print("- same day")
    else:
        wks.clear()
        wks.append_row(["PLATF", "TODAY", "DATE", "NAME", "RESERV", "SCORE", "PRICES"])

    return wks, wksInput


# --- Connects to Google API ---
def connect_to_google():
    print("\nConnecting to Google API")
    global wks, wksInput, sh

    try:
        file_path = os.path.realpath(Path(__file__).parent.parent / "config/credentials.json")

        credentials = service_account.Credentials.from_service_account_file(
            file_path, scopes=['https://www.googleapis.com/auth/drive'])
        goog = gspread.authorize(credentials)

        sh = goog.open(sheet.sheetName)
        wks = sh.worksheet(sheet.resultWorksheet)
        wksInput = sh.worksheet(sheet.settingsWorksheet)

    except Exception as error:
        exceptions.more_info("GOOGLE API FAILED!", error)

    return wks, wksInput


# --- Sends values to sheet ---
def send_values(finalList):
    print("\nSending values")
    global wks, sh

    try:
        emptyCell = len(wks.col_values(1)) + 1
        sh.values_update(f"{sheet.resultWorksheet}!A{emptyCell}", params={
            "valueInputOption": "RAW"}, body={"values": finalList})

    except TimeoutException as error:
        exceptions.simple("Timeout - failed to send values to sheet. Error:", error)

    except Exception as error:
        exceptions.more_info("Send values to sheet FAILED!", error)
