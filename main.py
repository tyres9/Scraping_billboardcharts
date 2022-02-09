from bs4 import BeautifulSoup
import requests

choice_date = input("Which year do you want to travel to? Type the date in this format.YYYY-MM-DD : ")

req = requests.get(f'https://www.billboard.com/charts/hot-100/{choice_date}/')
site_html = req.text
soup = BeautifulSoup(site_html, 'html.parser')

songs = soup.select(selector="li h3", id="title-of-a-story")
print(len(songs))
for song in songs[:100]:
    print(song.getText())


