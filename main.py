import csv
import os
from bs4 import BeautifulSoup as bs
import requests

def get_matches():
    matches = []
    with open('matches.txt') as match_input:
        reader = csv.reader(match_input, delimiter='-', quotechar='|')
        for row in reader:
            matches.append(row)

    return matches #return 2D array of matches (duels) we want to predict

def read_resfile(file,team1,team2):
    results = []

    with open(file) as stream:
        reader = csv.DictReader(stream)

        for row in reader:
            if team1 in row['HomeTeam'] and team2 in row['AwayTeam']:
                results.append(row['FTAG'] + ':' + row['FTHG'])
            elif team2 in row['HomeTeam'] and team1 in row['AwayTeam']:
                results.append(row['FTHG'] + ':' + row['FTAG'])

    return results #returns array of result from matchups between set teams

def get_results(matches):
    results = []

    for match in matches:
        results.append(read_resfile('csv/2019_2020.csv',match[1],match[0]))

    return results #return 2D array of results of matchups from the last season


def scrape_latest_results(team1,team2):
    results = []
    #url = 'https://www.skysports.com/premier-league-results'
    url = 'https://www.skysports.com/europa-league-results'
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')

    if 'No results currently available' in page.text:
        return None
    else:
        content = soup.find_all('div', class_='fixres__item')
        for item in content:
            t1 = item.find('span', class_='matches__item-col matches__participant matches__participant--side1')
            t2 = item.find('span', class_='matches__item-col matches__participant matches__participant--side2')
            res = item.find('span', class_='matches__teamscores')
            if team1 in t1.text or team2 in t2.text:
                result = [int(i) for i in res.text.split() if i.isdigit()]
                results.append(result)
            else:
                continue
    #čekovat minulé matchupy těch dvou zadaných týmů, přihlédnout k výsledku toho zápasu skrz nějaký koeficient (možná na to zrobit jinou funkci co to bude vracet samostatně)
    return results #returns 2D array of scraped results from this season

matches = get_matches()
#results = read_resfile('csv/2019_2020.csv',matches[1][1],matches[1][0])
print (matches)
print(get_results(matches))
print (scrape_latest_results('Apollon Limassol','Honka'))

print('-------')

try:
    for match in matches:
        results = scrape_latest_results(match[0],match[1])
        if results is None:
            print('No matches found for {} and {}'.format(match[0],match[1]))
        else:
            #logika statistické predikce
            print(match)
            print(teams)
            print(results)
            print('---')
except:
    print('ERROR')
