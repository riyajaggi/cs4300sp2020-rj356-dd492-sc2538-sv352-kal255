import requests
import pandas as pd
from bs4 import BeautifulSoup
import find_shows_in_ds
import os

session = requests.Session()

def makeSoup(url):
    res = session.get(url,timeout=5)
    res.raise_for_status()
    soup_content = BeautifulSoup(res.content, "lxml")
    for style in soup_content(["style"]):
        style.decompose()
    return soup_content

count = 0
for title, show_link in find_shows_in_ds.titles_to_links.items():
  count+=1
  show = title
  if ":" in show:
    show = show.replace(":", "")
  if "?" in show:
    show = show.replace("?", "")
  if "*" in show:
    show = show.replace("*", "")
  if "+" in show:
    show = show.replace("+", "")
  if "/" in show:
    show = show.replace("/", "")
  abbrev = show.lower().replace(" ","_")
  show_dir_path = "./transcripts2/" + show
  if not os.path.isdir(show_dir_path):
    os.mkdir(show_dir_path)

  url = show_link
  soup = makeSoup(url)
  episode_url = "https://subslikescript.com/"


  links = [episode_url + eps_link['href'][1:] for eps_link in soup.select("div.season a")]
  num_transcripts = 0
  for link in links:
    if num_transcripts <= 10:
      res = requests.get(link)
      html_page = res.content
      soup = BeautifulSoup(html_page, 'html.parser')
      text = soup.find_all(text=True)

      output = ''
      blacklist = [
          '[document]',
          'noscript',
          'header',
          'html',
          'meta',
          'head', 
          'input',
          'script',
          'style'
        ]

      split_url = link.split("/")
      season = split_url[5].split("-")[1]
      episode = split_url[6].split("-")[1]
      for t in text:
        if t.parent.name not in blacklist:
          output += '{} '.format(t)

      text_file = show_dir_path + "/" + abbrev + "_scripts_s"+ season +"_e"+ episode +".txt"
      write_file = open(text_file, "wt")
      write_file.write(output)
      write_file.close() 
      num_transcripts += 1
  print(count)
print("\nEND OF SCRIPT")

