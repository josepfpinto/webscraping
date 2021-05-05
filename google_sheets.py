import bin.config as Config
import gspread as Gs
from oauth2client.service_account import ServiceAccountCredentials


# --- Connects to Google API ---
def api_google():

    print ('Connecting to Google API')
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('bin/Google_API.json', scope)
    
    goog = Gs.authorize(credentials)
    
    sh = goog.open(Config.google_sheet)
    wks = goog.open(Config.google_sheet).sheet1
    wksInput = sh.get_worksheet(1)
    
    return wks, wksInput


def init(day):
    
    # Initiate Google API
    wks, wksInput = api_google()

    # Prepare Google Sheets
    print ('Preparing Google Sheets')

    if wks.acell('A1').value == 'PLATF' or wks.acell('A1').value == null:
        print ("- empty")
    elif wks.row_values(2)[1] == day:
        print ("- same day")
    else:
        wks.clear()
        wks.append_row(['PLATF', 'TODAY', 'DATE', 'NAME', 'RESERVAS', 'SCORE', 'PRICES', 'SUPERHOST'])

    return wks, wksInput

