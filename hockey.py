from bs4 import BeautifulSoup as bs
import requests
import csv
import statistics
from datetime import date

"""
def scrape_latest_results(team1,team2): #scrapes this season's results from the web
    results = []
    url = 'https://www.the-sports.org/ice-hockey-kontinental-hockey-league-khl-regular-season-2020-2021-results-eprd107270.html'
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')

    if 'No results currently available' in page.text:
        return None
    else:
        content = soup.find_all('tr')
        for item in content:
            if item.find('a', title=team1) or item.find('a', title=team2):
                res = item.find('b')
                if res is not None:
                    if "Postponed" in res.text:
                        continue
                    else:
                        result = [int(i) for i in res.text.split() if i.isdigit()] #odstranit prázdné arraye
                        results.append(result)
                else:
                    continue
            else:
                continue
    results = [x for x in results if x]
    return results #returns 2D array of scraped results from this season
"""

def read_resfile(file,team1,team2):
    results = []

    with open(file) as stream:
        reader = csv.DictReader(stream, delimiter=';')

        for row in reader:
            res = []
            result = row['RESULT'][:3].split()
            if team1 in row['HOME'] or team2 in row['VISITORS']:
                res.append(int(result[0][0]))
                res.append(int(result[0][2]))
                results.append(res)
            else:
                continue

    return results

def get_matches():
    matches = []
    with open('matches.txt') as match_input:
        reader = csv.reader(match_input, delimiter='-', quotechar='|')
        for row in reader:
            matches.append(row)

    return matches #return 2D array of matches (duels) we want to predict

def normalize_scores(matches): #takes 2D array of played matches, normalizes and returs the results in human-readable format
    scores = []
    for match in matches:
        scores.append('{}:{}'.format(match[0],match[1]))
    
    return scores

matches = get_matches()
#print(read_resfile('csv/khl_2020_09_15.csv','Barys Nur-Sultan','Salavat Yulaev Ufa'))
resfile = 'csv/khl_2020_09_15.csv'
print('Goal Count Predictor by Dominik Zarsky (https://github.com/Loupeznik)')
print('Project is MIT licensed')
print('Version 0.9 - Hockey')
print('Last updated 2020-09-16')
print('----------------------------')

try:
    for match in matches:
        results = read_resfile(resfile,match[0],match[1])
        if results is None:
            print('No matches found for {} and {} this season'.format(match[0],match[1]))
        else:
            #logika statistické predikce
            print('Prediction model for {} vs {} as of {}'.format(match[0],match[1],date.today()))
            goalcount = []
            for result in results:
                goalcount.append(sum(result))
            average_goals = sum(goalcount)/len(goalcount)
            maximum = max(goalcount)
            minimum = min(goalcount)
            minimal_safe_number = (minimum + maximum) / average_goals
            print('Average goalcount in this season\'s matchups of {} and {} is {}'.format(match[0],match[1],round(average_goals, 1)))
            print('Minimal safe number of goals scored in the next matchup was predicted to be {}'.format(round(minimal_safe_number, 1)))
            print('----------------------------')
except:
    print('ERROR')
