isDB
===
# Scraping Tools
These are tools for scraping links and text from an international scholarship database.

## scrape_isd_links.py
This scrapes the urls to individual records of the database from a search page

## scrape_isd_scholarships.py
This uses the urls from the previous script to capture individual scholarship text.

## scrape_scholarship_link_tos.py
This uses the urls from the individual scholarship pages, which link to the source pages at universities
and other groups. The html is saved.

## html_to_csv
This uses BeautifulSoup and some manual text processing algorithms to extract meaningful text
from the saved html files, then exports them to a .csv file, for future use with Deepdive.

#scrape_google_search.txt
a simple script using the xgoogle library to scrape the links from a google search results page
