#TODO:
#   Handle possible exceptions

import requests
import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

#INPUTS
YEAR = 2023
KEY = "3a68398efff43f93cee5e0addb6597e78dc93a31" #CHANGE TO BE GROUP KEY

#get filepath
filepath = os.path.dirname(__file__)

#Build API URL
URL = "https://api.census.gov/data/"
URL += str(YEAR)
URL += "/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:49&key="
URL += KEY

#request the API
req = requests.get(URL)
req.raise_for_status()

#create empty dataframe
df = pd.DataFrame(columns=["County", "Median Income"])

#iterate through request data, add data to dataframe
for line in req.json():
    if "Utah" not in line[0]:
        continue
    df.loc[len(df)] = [line[0][:-13], int(line[1])]

print(df)


#BRAD'S PUSHING CODE

# Load your credentials JSON file
SERVICE_ACCOUNT_FILE = filepath + '/asctrib-80f6887f88b8.json'  # path to your file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open Google Sheet (by name or ID)
sheet = client.open("ASC Test Sheet").sheet1  # opens the first sheet

# Clear the existing content
sheet.clear()

# Push headers + rows
sheet.update([df.columns.values.tolist()] + df.values.tolist())