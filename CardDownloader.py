import sys # For command line arguments
import json # For parsing the json input file
import requests # For connecting to the web page and downloading the image
import shutil # For reading and saving the image
from bs4 import BeautifulSoup # For parsing the web page

fileName = sys.argv[1]
print('Chosen file: ' + fileName)

with open(fileName) as json_data:
    data = json.load(json_data)

for (k, v) in data['results'].items():
    page = requests.get('https://yugioh.fandom.com/wiki/' + k.replace(' ', '_'))
    soup = BeautifulSoup(page.text, 'html.parser')
    card = soup.find(class_='cardtable-cardimage');
    img = card.find('img')['src']

    link = ''
    if '.png' in img:
        link = img[:img.find('.png/') + 4]
    elif '.jpg' in img:
        link = img[:img.find('.jpg/') + 4]
    
    if link != '':
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            with open(link[link.rfind('/')+1:], 'wb') as f:
                for chunk in r:
                    f.write(chunk)

        print('Saved: ' + link[link.rfind('/')+1:])
    else:
        print('Error downloading: ' + img)