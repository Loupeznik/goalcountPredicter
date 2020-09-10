import csv
import os
from bs4 import BeautifulSoup as bs
import requests
import statistics
from datetime import date

def get_matches():
    matches = []
    with open('matches.txt') as match_input:
        reader = csv.reader(match_input, delimiter='-', quotechar='|')
        for row in reader:
            matches.append(row)

    return matches #return 2D array of matches (duels) we want to predict

def read_resfile(file,team1,team2): #reads results of given teams from last year's match records
    results = []

    with open(file) as stream:
        reader = csv.DictReader(stream)

        for row in reader:
            result = []
            if team1 in row['HomeTeam'] and team2 in row['AwayTeam']:
                result.append(int(row['FTHG']))
                result.append(int(row['FTAG']))
                results.append(result)
            elif team2 in row['HomeTeam'] and team1 in row['AwayTeam']:
                result.append(int(row['FTAG']))
                result.append(int(row['FTHG']))
                results.append(result)

    return results #returns array of result from matchups between set teams

def scrape_latest_results(team1,team2): #scrapes this season's results from the web
    results = []
    #url = 'https://www.skysports.com/premier-league-results'
    url = 'https://www.skysports.com/scottish-premier-results' #testcases
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

def normalize_scores(matches): #takes 2D array of played matches, normalizes and returs the results in human-readable format
    scores = []
    for match in matches:
        #scores.append(str(match[0]) + ':' + str(match[1]))
        scores.append('{}:{}'.format(match[0],match[1]))
    
    return scores

matches = get_matches()
#resfile = 'csv/2019_2020.csv'
resfile = 'csv/scottish_premiership_2019_2020.csv' #testcases
#results = read_resfile(resfile,matches[1][0],matches[1][1])
#print(results)
#print(normalize_scores([[2,2],[2,10],[1,5]]))
print('Goal Count Predictor by Dominik Zarsky (https://github.com/Loupeznik)')
print('Project is MIT licensed')
print('Version 1.0')
print('Last updated 2020-09-10')
print('----------------------------')

try:
    for match in matches:
        results = scrape_latest_results(match[0],match[1])
        if results is None:
            print('No matches found for {} and {} this season'.format(match[0],match[1]))
        else:
            #logika statistické predikce
            print('Prediction model for {} vs {} as of {}'.format(match[0],match[1],date.today()))
            goalcount = []
            for result in results:
                goalcount.append(sum(result))
            average_goals = sum(goalcount)/len(goalcount)
            #median = statistics.median(goalcount) #not behaving well in the current model, might have use for this later
            maximum = max(goalcount)
            minimum = min(goalcount)
            minimal_safe_number = (minimum + maximum) / average_goals
            #print('MINIMUM: {} MAXIMUM: {} MEDIÁN: {} PRŮMĚR: {}'.format(minimum,maximum,median,average_goals)) #debug
            print('Average goalcount in this season\'s matchups of {} and {} is {}'.format(match[0],match[1],round(average_goals, 1)))
            print('Minimal safe number of goals scored in the next matchup was predicted to be {}'.format(round(minimal_safe_number, 1)))
            try:
                last_season_matchups = read_resfile(resfile,match[0],match[1])
                if not last_season_matchups:
                    print('No last season matchup was found for {} and {}'.format(match[0],match[1]))
                else:
                    last_season_goals = []
                    last_season_scores = normalize_scores(last_season_matchups)
                    for stat in last_season_matchups:
                        stat = sum(stat)
                        last_season_goals.append(stat)
                    last_season_avg_goals = sum(last_season_goals)/len(last_season_goals)
                    #print(last_season_avg_goals)
                    print('Matchups from last season resulted in {} average goals per match, with the scores being {}'.format(round(last_season_avg_goals, 1),', '.join(last_season_scores)))
            except:
                print('There was an error fetching the last season result sheet (check if it is present in the /csv folder)')
            print('----------------------------')
except:
    print('ERROR')
