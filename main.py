import os
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import glob

link = 'https://www.carmudi.co.id/mobil-dijual/indonesia?'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}


def scrap(page):
    params = {
        'page_number': page,
        'page_size': 50
    }
    req = requests.get(link, params=params, headers=headers)

    data = []

    soup = BeautifulSoup(req.text, 'html.parser')
    mainsoup = soup.find_all('div', 'flex flex--row flex--wrap')

    # create folder for file
    try:
        os.mkdir('resultfile')
        os.mkdir('resultfile/jpgfile')
        os.mkdir('resultfile/file')
        os.mkdir('resultfile/file/json')
        os.mkdir('resultfile/file/excelcsv')
    except FileExistsError:
        pass

    # scraping
    for i in mainsoup:
        # accsess link for full description
        links = i.find('a', 'ellipsize js-ellipsize-text')['href']
        reqtwo = requests.get(links)
        souptwo = BeautifulSoup(reqtwo.text, 'html.parser')

        title = i.find('a', 'ellipsize js-ellipsize-text').text.strip().replace('/', '')

        # handling error for ads that have no price
        try:
            price = i.find('div', 'listing__price delta weight--bold').text
        except Exception:
            price = 'Best Deal'

        # handling error for src other than image
        try:
            img = i.find('a', 'listing__overlay one-whole inline--block valign--top relative').find('img')['data-src']
        except Exception:
            pass

        # handling error for unavailable description
        try:
            desc = souptwo.find('span', {'itemprop': 'description'}).text.replace('\n', ' ').replace('Tawaran Terbaik dari Carmudi.co.id ', '')
        except Exception:
            pass

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
            'loc': loc,
            'link': links
        }
        data.append(datt)
        print(f"{title}. Price: {price}. image: {img} \ndescription: {desc}.\n{km}\n{trans}transmition\nloc: {loc}\nlink: {links}")

        # download image
        with open(f'resultfile/jpgfile/{title}.jpg', 'wb') as outfile:
            imggg = requests.get(img)
            outfile.write(imggg.content)

    # create json
    with open(f'resultfile/file/json/json page {page}.json', 'w+') as jsonfile:
        json.dump(data, jsonfile)
        print('json file was created')

    # create excel & csv file
    df = pd.DataFrame(data)
    df.to_csv(f'resultfile/file/excelcsv/csv page {page}.csv', index=False)
    df.to_excel(f'resultfile/file/excelcsv/excel page {page}.xlsx', index=False)
    print('excel & csv file was created')


def run():
    try:
        option = int(input('choose your option: \n1. get spesific page \n2. get all page (1-100)\ninput here: '))
    except Exception:
        print('choose valid option number you want')
        return run()

    if option == 1:
        try:
            a = int(input('input your spesific page: '))
            if a > 0:
                scrap(a)
            else:
                print('frist page is one, please re enter your spesific page')
                return run()
        except Exception:
            print('please enter a valid number for the page')
            return run()

    elif option == 2:
        for j in range(1, 101):
            scrap(j)
        try:
            os.mkdir('resultfile/file/alldatafile')
        except FileExistsError:
            pass

        # read json file for merge
        filesjson = sorted(glob.glob('resultfile/file/json/*.json'))
        datas = []
        for i in filesjson:
            with open(i) as jsonfile:
                data = json.load(jsonfile)
                datas.extend(data)

        # create merge excel csv file
        df = pd.DataFrame(datas)
        df.to_csv('resultfile/file/alldatafile/all data csv.csv', index=False)
        df.to_excel('resultfile/file/alldatafile/all data excel.xlsx', index=False)

        # create merge json file
        with open('resultfile/file/alldatafile/result_all_data_json.json', 'w') as outfile:
            json.dump(datas, outfile)

    else:
        print('please enter valid number for option number')
        return run()


run()
