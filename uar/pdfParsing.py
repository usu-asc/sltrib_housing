#imports
import pypdf
import os
import gspread
from google.oauth2.service_account import Credentials

#get current filepath
filepath = os.path.dirname(__file__)

#functions
def read_pdf(pdfPath): #extracts the text of a pdf
    with open(pdfPath, 'rb') as file:
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

#assign target pdf
targetPDF = "UARdata_01_2025.pdf"

#read text and split into list
text = read_pdf(filepath + "/" + targetPDF)
text = text.split("\n")

#remove uneccesary lines
textList = []
for line in text:
    if (("+" in line) or ("-" in line)) and ("Entire State" not in line):
        textList.append(line)

#parse out headers
lineOne = textList.pop(0)
headers = lineOne.split(" ")

cleanedHeaders = []
for i in range(len(headers)):
    if (headers[i] != "-") and ("-" in headers[i]):
        cleanedHeaders.append(headers[i])
    elif headers[i] == "+":
        cleanedHeaders.append("+/-")
    elif headers[i] == "YTD":
        cleanedHeaders.append(headers[i-1] + " YTD")

#clean data
data = []

for line in textList:
    lineList = line.split(" ") #split line into list

    #initialize loop variables
    county = False
    dataList = []
    for i in range(len(lineList)): #format line list into a line of clean data

        if lineList[i] == "County":
            dataList.append(" ".join(lineList[:i+1])) #append county name to data
            county = True
            continue #avoid double appending the word County
        if not county: #don't parse data until county has been parsed
            continue
        if (lineList[i] != "+") and (lineList[i] != "-"): #avoid appending +/- to incorrect rows
            if (lineList[i-1] == "+") or (lineList[i-1] == "-"): #make sure +/- get attached to the right data
                dataList.append("".join(lineList[i-1:i+1]))
            else:
                dataList.append(lineList[i])
        
    data.append(dataList) #add line of cleaned data to data list

#add headers to data
data.insert(0, cleanedHeaders)


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
sheet.update(data)