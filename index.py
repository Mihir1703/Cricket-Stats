import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import csv

base_url = 'https://www.cricbuzz.com/api/search/results?q='
base_url_2 = 'https://www.cricbuzz.com/profiles/'
image_url = 'https://www.cricbuzz.com'

players = pd.read_csv('players.csv', header=None)
players = [i[0] for i in players.values.tolist()]

not_found = csv.writer(open('not_found.csv', 'w+', newline='\n'))
bat = csv.writer(open('player_bat.csv', 'a+', newline='\n'))
bowl = csv.writer(open('player_bowl.csv', 'a+', newline='\n'))
image = csv.writer(open('player_image.csv', 'a+', newline='\n'))

bat.writerow(['Name', 'Mat', 'Inns', 'NO', 'Runs', 'HS',
             'Avg', 'BF', 'SR', '100', '50', '4s', '6s'])
bowl.writerow(['Name', 'Mat', 'Inns', 'Balls', 'Runs', 'Wkts',
              'BBI', 'Avg', 'Econ', 'SR', '5w', '10w'])
image.writerow(['Name', 'Type','Image'])

for i in players:
    try:
        print(base_url + '%20'.join(str(i).lower().split(' ')))
        respo = requests.get(base_url + '%20'.join(str(i).lower().split(' ')), headers={
                             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
        respo = json.loads(respo.text)
        if respo == None:
            respo = requests.get(base_url + '-'.join(str(i).lower().split(' ')), headers={
                                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            respo = json.loads(respo.text)
        respo = respo['playerList'][0]['id']
        url = base_url_2 + str(respo)
        # print(url)
        respo = requests.get(url, headers={
                             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
        soup = bs(respo.text, 'html.parser')
        imgs = ""
        try:
            imgs = image_url + soup.find_all(title="profile image")[0]['src']
        except:
            imgs = 'Not Found'
        typ = ""
        try:
            typ = str(soup.find_all('div', {'class': 'cb-col cb-col-60 cb-lst-itm-sm'})[2].get_text()).replace(' ','')
        except:
            typ = "Not Found"
        soup = soup.find_all('tbody')
        ba = True
        for y in soup:
            data = y.find_all('tr')[-1]
            store = [i]
            for k in data.find_all('td')[1:]:
                if k.text == '-':
                    store.append(0)
                else:
                    store.append(k.text)
            if ba:
                print(store)
                bat.writerow(store)
            else:
                print(store)
                bowl.writerow(store)

            ba = False
        image.writerow([i, typ,imgs])
    except Exception as e:
        not_found.writerow([i])
        print(i + ' Not found')
        print(e)
        pass
