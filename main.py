import datetime as Date
from pandas.tseries.offsets import BusinessDay

from services import g_driver, new_url, webpage_scraping as WebScrap, google_sheets as Gsheets

# --- Main Program ---
if __name__ == "__main__":

    day = Date.datetime.today().strftime("%d-%m-%Y")
    wks, wksInput = Gsheets.init(day)
    g_driver.init()

    # Get User Data
    dateIn = Date.datetime.strptime(
        wksInput.acell("H5").value, "%d-%m-%Y").date()
    months = int(wksInput.acell("I5").value)
    totalDays = int(wksInput.acell("K5").value)
    totalAdults = str(wksInput.acell("L5").value)
    cleaningFee = int(wksInput.acell("M5").value)

    # Find and Copy Values to Sheet
    print("\nSTART!")

    i = 0
    while i < months:
        print("---- ", dateIn, " ----")
        new_url.get(dateIn, totalDays, totalAdults)
        WebScrap.loop_pages(day, dateIn, totalDays, cleaningFee, totalAdults)
        dateOut = dateIn + BusinessDay(20) if i % 2 == 0 else dateIn + BusinessDay(25)
        dateIn = dateOut.date()
        i += 1

    # g_driver.close()
