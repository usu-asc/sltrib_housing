#TODO:
#   Get API key for project
#   Setup upload to google sheets
#   Handle possible exceptions

import requests
import os

#INPUTS
YEAR = 2024
KEY = "6e2b95431f299e56cb3bca8359ccae1cf3b2604f" #CHANGE TO BE GROUP KEY

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

#create empty list to store JSON data
jsonLines = []

#iterate through request data, add data to JSON lines
for line in req.json():
    if "Utah" not in line[0]:
        continue
    jsonLines.append('"' + line[0][:-13] + '", ' + line[1] + "\n")

#write JSON lines to file
with open(filepath + "\census.csv", "w") as file:
    file.writelines(jsonLines)