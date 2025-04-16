import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.tfrrs.org/all_performances/MN_college_m_Carleton.html?list_hnd=5027&season_hnd=681"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

page = requests.get(url, headers = headers)






soup = BeautifulSoup(page.content, "html.parser")



eventList = {}

results = {}


links = soup.find(id = "quick-links-list")   #gets the list of each event and the name of the event they refer to

cells = links.find_all("a")    #gets the actual events
for cell in cells:
    eventList[cell['href'][1:]] = cell.text  #organizes it into a key value pairing , e.g "event6 : 100"


for event in eventList: #creates a key value pairing such that each event has a corresponding beautifulsoup w/ all the event inputs
    results[eventList[event]] = soup.find(id = event).find_next_sibling("div")
   


with open("output1.html", "wb") as file:  #writes to file for testing,, each event shows up. We can just select necessary values
    for result in results:
        text = results[result].prettify("utf-8")
        file.write(text)
       



# <li><a data-turbo="false" href="#event6">100</a></li>
      #  <li><a data-turbo="false" href="#event7">200</a></li>
      #  <li><a data-turbo="false" href="#event11">400</a></li>
      #  <li><a data-turbo="false" href="#event12">800</a></li>
      #  <li><a data-turbo="false" href="#event13">1500</a></li>
      #  <li><a data-turbo="false" href="#event21">5000</a></li>
      #  <li><a data-turbo="false" href="#event5">110H</a></li>
      #  <li><a data-turbo="false" href="#event9">400H</a></li>
      #  <li><a data-turbo="false" href="#event19">3000S</a></li>
      #  <li><a data-turbo="false" href="#event31">4x100</a></li>
      #  <li><a data-turbo="false" href="#event33">4x400</a></li>
      #  <li><a data-turbo="false" href="#event23">HJ</a></li>
      #  <li><a data-turbo="false" href="#event24">PV</a></li>
      #  <li><a data-turbo="false" href="#event25">LJ</a></li>
     #   <li><a data-turbo="false" href="#event26">TJ</a></li>
    #    <li><a data-turbo="false" href="#event30">SP</a></li>
   #     <li><a data-turbo="false" href="#event27">DT</a></li>
  #      <li><a data-turbo="false" href="#event29">JT</a></li>
 #       <li><a data-turbo="false" href="#event39">Dec</a></li>
#