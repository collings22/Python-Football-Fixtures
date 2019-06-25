#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

url = "https://www.skysports.com/middlesbrough"

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

block_fixtures = soup.find(class_='matches-block__match-list')

fixture_list_dates = block_fixtures.find_all('h4')
fixture_list_home = block_fixtures.find_all(class_='matches__item-col matches__participant matches__participant--side1')
fixture_list_away = block_fixtures.find_all(class_='matches__item-col matches__participant matches__participant--side2')

game_status = block_fixtures.find_all(class_='matches__status')

fixtureResults = dict()
for idx, each in enumerate(fixture_list_dates):
    key = each.text.strip()
    game_stat = game_status[idx].text.strip().replace(" ","")
    if("inplay" in game_stat):
        game_stat = game_stat.replace("inplay","").replace("\n\n","")
    else:
        game_stat = game_stat.replace("\n\n","-")
    fixtureResults[key] = (fixture_list_home[idx].text.strip(), game_stat ,fixture_list_away[idx].text.strip())

fixtureResults

df = pd.DataFrame(fixtureResults).T

df.rename(columns={0:"Home",1:"KO/Result",2:"Away"}, inplace=True)

df

