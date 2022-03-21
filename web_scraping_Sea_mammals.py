
######      # setup
import requests   
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import os
import urllib3

#####       # predefined parameteres 

audioDir = './Data'

## website to import data
# URL_Data=[]
# URL_Data.append("https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=BD15F")

# or dictionary 
URL_Data = {
    "spotted Dolphin": "https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=BD15F",
    "Bearded Seal": "https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=CC2A",
    "Beluga White Whale": "https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=BB1A",
    "Bottlenose Dolphin":"https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=BD19D",
    "Bowhead Whale":"https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=AA1A",
    "Clymene Dolphin":"https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=BD15B",
    "Common Dolphin" :"https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=BD3B",
    "BFalse Killer Whale":"https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=BE9A",
    "Finback Whale":"https://whoicf2.whoi.edu/science/B/whalesounds/bestOf.cfm?code=AC1F",
    }


#####       # list all download links for .wav file

def scrappingDownloadURL(URL_Data):
    req = requests.get(URL_Data)
    soup = BeautifulSoup(req.content, "html")
    URL_Download = [a['href'] for a in soup.find_all('a',href=re.compile(".wav"))]
    return URL_Download
    
    # # for debugging
    # import webbrowser
    # webbrowser.open(URL_Data, new=2)
    # print(soup.prettify())
    # div = soup.find("div", {"class": "database"})
    # table = div.find("table")
    # print(table)
    # print(URL_Download)


######      # Download audio files

def downloadAudio(URL_Download,downloadDir):

    for url in URL_Download:
        DL_Dir = os.path.join(downloadDir,url.split('/')[-1])

        LD_req = requests.get(f'https://whoicf2.whoi.edu{url}')
        
        with open(DL_Dir, 'wb') as f:
            f.write(LD_req.content)

        print('downlead completed:'+DL_Dir)




#####       #webs crapping fore each marine creature in dictionary

if not os.path.exists(audioDir): # if no data folder create a directory
    os.makedirs(audioDir)

for key in URL_Data:
    downloadDir = os.path.join(audioDir,key)
    if not os.path.exists(downloadDir): # if no sub-folder create a directory
        os.makedirs(downloadDir)
    
    URL_Download = scrappingDownloadURL(URL_Data[key])
    downloadAudio (URL_Download,downloadDir)

