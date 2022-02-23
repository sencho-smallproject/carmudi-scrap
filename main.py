from bs4 import BeautifulSoup
import requests

link = 'https://www.carmudi.co.id/mobil-dijual/indonesia?'

page = input('input page scrap: ')

params = {
    'page_number': page,
    'page_size': 25
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
req = requests.get(link, params=params, headers=headers)

soup = BeautifulSoup(req.text, 'html.parser')
mainsoup = soup.find_all('div', 'flex flex--row flex--wrap')

for i in mainsoup:
    title = i.find('a', 'ellipsize js-ellipsize-text').text.strip()
    price = i.find('div', 'listing__price delta weight--bold').text.strip()
    img = i.find('a', 'listing__overlay one-whole inline--block valign--top relative').find('img')['data-src']
    print(f"{title}. Price: {price}. image: {img}")






