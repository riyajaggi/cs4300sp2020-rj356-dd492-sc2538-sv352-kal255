import requests
from bs4 import BeautifulSoup
import json
import transcripts_info

def makeSoup(url):
    res = session.get(url,timeout=5)
    res.raise_for_status()
    soup_content = BeautifulSoup(res.content, "lxml")
    for style in soup_content(["style"]):
      style.decompose()
    return soup_content

titles_to_links = {}

tv_shows = transcripts_info.tv_shows_no_transcripts
letter = 'Z'

url = "https://subslikescript.com/series_letter-"+ letter
soup = makeSoup(url)
pages = 0

for link in soup.select("a.page-link"):
  page_number = link.contents[0]
  if page_number.isnumeric():
    pages = int(page_number)

for i in range(1, pages+1):
  letter_page_url = "https://subslikescript.com/series_letter-"+letter+"?page=" + str(i)
  page_soup = makeSoup(letter_page_url)
  show_url = "https://subslikescript.com/"
  for link in page_soup.select("ul.scripts-list a"):
    title = link.contents[0].contents[0].split(" (")[0]
    if title in tv_shows:
      titles_to_links[title] = show_url + link['href'][1:]

print(titles_to_links)
print(len(titles_to_links))
print("\nEND OF SCRIPT")