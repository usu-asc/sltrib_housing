import pdfplumber
import pandas as pd
import re

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

import os
import requests as req

### PULL DATA

#constants
MONTH_TEXT = ["NA", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

#get path
path = os.path.dirname(__file__)

#----INPUTS----
#define target year and month
targetYear = 2025
targetMonth = 1

#define guess year and month
guessYear = targetYear
guessMonth = targetMonth

#get target strings for URL
targetYear = str(targetYear)
targetMonth = MONTH_TEXT[targetMonth]

#MAIN LOOP
responseCode = 403
while responseCode == 403:
    #build url
    guessYearText = str(guessYear)
    guessMonthText = MONTH_TEXT[guessMonth]

    #request url, update responseCode
    r = req.get("https://utrealtors.wpenginepowered.com/wp-content/uploads/" + guessYearText + "/" + guessMonthText + "/All-Counties_" + targetYear + "-" + targetMonth + ".pdf")
    responseCode = r.status_code

    #update guess of upload date
    guessMonth += 1
    if guessMonth > 12:
        guessMonth = 1
        guessYear += 1

#open the target file and write the data
with open(path + '/UAR_' + targetMonth + '_' + targetYear + '.pdf', 'wb') as test:
    test.write(r.content)