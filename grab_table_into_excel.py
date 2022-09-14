from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Download the chrome driver correspond to your Google Chrome version
# put in the same file / directory of this python file
# https://chromedriver.chromium.org/downloads

# Selenium is used to click search button to generate the search result of the 
browser = webdriver.Chrome()
url = 'https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en'
browser.get(url)

# Your can find the HTML element by mouse right click -> inspect / F12
# find_element is to search by the class / id / div of html element
search_button = browser.find_element(By.XPATH,"//a[@class = 'filter_btn-applyFilters-js btn-blue']").click()

# Get all html element to beautifulsoup for faster computation
soup = BeautifulSoup(browser.page_source,"lxml")

# if you need to load more, can create scroll down and click load more
# But this code just stop here on the first page
browser.close()

# get table
table = soup.find("table",
                  {"class":"table sticky-header-table table-scroll table-mobile-list tablesorter tablesorter-default tablesorterc22739541e743 hasStickyHeaders"})
# get one row only
# you may need a loop to get all rows in table
release_time = table.find("td",{"class":"text-right release-time"}).text
stock_code = table.find("td",{"class":"text-right stock-short-code"}).text
headline = table.find("td",{"class":"headline"}).text
doc_link = table.find("td",{"class":"doc-link"})

# in case you want to download the document
doc_link_back = doc_link.find("a").get('href')
doc_link_front = 'https://www1.hkexnews.hk'

whole_doc_link = doc_link_front + doc_link_back

lst = []
lst.append(release_time)
lst.append(stock_code)
lst.append(headline)
lst.append(whole_doc_link)

df = pd.DataFrame(lst,columns=['release_time','stock_code','headline','url'])

df.to_csv('listed_company_info.csv',index=False)
