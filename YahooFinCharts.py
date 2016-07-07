#! Yahoo Finance Chart Scraper
# Download financial information from Yahoo Finance

import requests as req
import os, bs4

url = input('Enter Yahoo Finance URL: ')

os.makedirs('Scraped data', exist_ok=True)

res = req.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")
elem = soup.select('#yfi_summary_chart img')

if elem == []:
    print('No chart')
else:

    charturl = elem[0].get('src')
    print('Downloading image %s...' % (charturl))
    res = req.get(charturl)
    res.raise_for_status()
        

    chartfile = open(os.path.join('Scraped data',input('File name: ')),'wb')

    for chunk in res.iter_content(100000) :
        chartfile.write(chunk)
    chartfile.close()
    
    
                     
