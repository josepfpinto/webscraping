import bin.config as config
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# --- Connects to Google API ---
def api_google():

    print ('Connecting to Google API')
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('bin/Google_API.json', scope)
    
    goog = gspread.authorize(credentials)
    
    sh = goog.open(config.google_sheet)
    wks = goog.open(config.google_sheet).sheet1
    wksInput = sh.get_worksheet(1)
    
    return wks, wksInput


def init():
    
    # Initiate Google API
    wks, wksInput = api_google()

    # Prepare Google Sheets
    print ('Preparing Google Sheets')

    if len(wks.row_values(2)) > 1 and wks.row_values(2)[1] == day:
        print ("SAME DAY!")
    else:
        wks.clear()
        wks.append_row(['PLATF', 'TODAY', 'DATE', 'NAME', 'RESERVAS', 'SCORE', 'PRICES', 'SUPERHOST'])

    return wks, wksInput

