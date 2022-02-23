import os
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd

link = 'https://www.carmudi.co.id/mobil-dijual/indonesia?'

page = input('input page scrap: ')

params = {
    'page_number': page,
    'page_size': 25
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
req = requests.get(link, params=params, headers=headers)

data = []

soup = BeautifulSoup(req.text, 'html.parser')
mainsoup = soup.find_all('div', 'flex flex--row flex--wrap')

for i in mainsoup:
    title = i.find('a', 'ellipsize js-ellipsize-text').text.strip()
    price = i.find('div', 'listing__price delta weight--bold').text
    img = i.find('a', 'listing__overlay one-whole inline--block valign--top relative').find('img')['data-src']
    desc = i.find('div', 'listing__excerpt milli text--muted push-quarter--ends').text.replace('...', ' read more').strip()
    km = i.find('i', 'icon icon--secondary muted valign--top push-quarter--right icon--meter').next_sibling
    trans = i.find('i', 'icon icon--secondary muted valign--top push-quarter--right icon--transmission').next_sibling
    loc = i.find('i', 'icon icon--secondary muted valign--top push-quarter--right icon--location').next_sibling

    datt = {
        'title': title,
        'price': price,
        'img': img,
        'desc': desc,
        'km': km,
        'trans': trans,
        'loc': loc
    }
    data.append(datt)
    print(f"{title}. Price: {price}. image: {img} \ndescription: {desc}.\n{km}\n{trans}transmition\nloc: {loc}\n")

    # download image
    with open(f'resultfile/{title}.jpg', 'wb') as a:
        imggg = requests.get(img)
        a.write(imggg.content)

# create folder for file
try:
    os.mkdir('resultfile')
except FileExistsError:
    pass

# create json
with open(f'resultfile/json page {page}.json', 'w+') as jsonfile:
    json.dump(data, jsonfile)
print('json file was created')

# create excel & csv file
df = pd.DataFrame(data)
df.to_csv(f'resultfile/csv page {page}.csv', index=False)
df.to_excel(f'resultfile/excel page {page}.xlsx', index=False)
print('excel & csv file was created')







