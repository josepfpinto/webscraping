import sys
import os
import bin.config as Config
import gspread as Gs
from selenium.common.exceptions import TimeoutException
from oauth2client.service_account import ServiceAccountCredentials


wks = ""
wksInput = ""
sh = ""


# --- Connects to Google Sheets and prepares sheets ---
def init(day):

    # Initiate Google API
    global wks, wksInput
    api_google()

    # Prepare Google Sheets
    print("\nPreparing Google Sheets")

    if wks.acell("A1").value == "PLATF" and wks.acell("A1").value == "":
        print("- sheet empty")
    elif wks.row_values(2)[1] == day:
        print("- same day")
    else:
        wks.clear()
        wks.append_row(["PLATF", "TODAY", "DATE", "NAME",
                       "RESERV", "SCORE", "PRICES", "SUPERHOST"])

    return wks, wksInput


# --- Connects to Google API ---
def api_google():

    print("\nConnecting to Google API")
    global wks, wksInput, sh

    try:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "bin/Google_API.json", scope)

        goog = Gs.authorize(credentials)

        sh = goog.open(Config.google_sheet)
        wks = goog.open(Config.google_sheet).sheet1
        wksInput = sh.get_worksheet(1)

    except Exception as error:
        print("\nError | GOOGLE API FAILED!")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, " ", error)

    return wks, wksInput


# --- Sends values to sheet ---
def send_values(finalList):

    print("\nSending values")
    global wks, sh

    try:
        emptyCell = len(wks.col_values(1)) + 1
        sh.values_update("Sheet1!A{}".format(emptyCell), params={
                         "valueInputOption": "RAW"}, body={"values": finalList})

    except TimeoutException as error:
        print("\nTimeout - failed to send values to sheet. Error: ", error)

    except Exception as error:
        print("\nError | Send values to sheet FAILED!")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, " ", error)
