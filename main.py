import csv
import os

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


matches = get_matches()
#results = read_resfile('csv/2019_2020.csv',matches[1][1],matches[1][0])
print (matches)
print(get_results(matches))
