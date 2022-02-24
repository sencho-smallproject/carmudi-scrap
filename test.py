import requests
from bs4 import BeautifulSoup

mainlink = 'https://www.carmudi.co.id/mobil-dijual/indonesia?'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
params = {
    'page_number': 1,
    'page_size': 25
}


mainreq = requests.get(mainlink, params=params, headers=headers)
soup = BeautifulSoup(mainreq.text, 'html.parser')

mainsoup = soup.find_all('div', 'flex flex--row flex--wrap')

for i in mainsoup:
    link = i.find('a', 'ellipsize js-ellipsize-text')['href']

    # access link
    reqq = requests.get(link)
    soupp = BeautifulSoup(reqq.text, 'html.parser')
    desc = soupp.find('span', {'itemprop': 'description'}).text.replace('\n', ' ')

