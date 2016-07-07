#! SEC Edgar Excel File Downloader
# Downloads most recent set of financial statements to a folder
# named "Scraped data" in the same folder as this script

import os, bs4, requests as req, time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

stock = input('What ticker do you want? ')

browser = webdriver.Firefox()
browser.get('https://www.sec.gov/edgar/searchedgar/companysearch.html')
searchelem = browser.find_element_by_id('cik')
searchelem.send_keys(stock)
searchelem.submit()

try:
    iselem = browser.find_element_by_xpath("//a[@id ='interactiveDataBtn']")
    iselem.click()
    
except NoSuchElementException:
    print('This fucker does not use xbrl')
    browser.quit()
    raise SystemExit

url = browser.current_url

res = req.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")
elem = soup.select('a[href$=".xlsx"]')

if elem == []:
    print('No Excel File')
else:
    exraw = elem[0].get('href')
    exfile = 'https://www.sec.gov' + exraw

    print('Downloading Excel File: %s...' % os.path.basename(exfile))
    res = req.get(exfile)
    res.raise_for_status()

    os.makedirs('Scraped data', exist_ok=True)

    chartfile = open(os.path.join('Scraped data', os.path.basename(exfile)),'wb')

    for chunk in res.iter_content(150000) :
        chartfile.write(chunk)
    chartfile.close()

    browser.quit()
    
    print('Done!')



    



