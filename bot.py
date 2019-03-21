import praw
import pytz
import sys, os
import json
import getpass
import random as r
import requests
import numpy as np
import re
from html.parser import HTMLParser
from time import sleep
from datetime import datetime, timedelta
from string import digits
import html2text
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pyimgur
import math
import traceback


def ordinal(n):
    return "%d^%s" % (n, "tsnrhtdd"[(math.floor(n/10) % 10 != 1)*(n % 10 < 4) * n % 10::4])


class Auto_Updater_Bot(object):
    def __init__(self, r, imgur, heavy=False):
        self.teams = {'VGK': ['/r/goldenknights', 'Vegas', 'Golden Knights'],
                      'MIN': ['/r/wildhockey', 'Minnesota', 'Wild'], 'TOR': ['/r/leafs', 'Toronto', 'Leafs'],
                      'WSH': ['/r/caps', 'Washington', 'Capitals'], 'BOS': ['/r/bostonbruins', 'Boston', 'Bruins'],
                      'DET': ['/r/detroitredwings', 'Detroit', 'Red Wings'],
                      'NYI': ['/r/newyorkislanders', 'New York', 'Islanders'],
                      'FLA': ['/r/floridapanthers', 'Florida', 'Panthers'],
                      'COL': ['/r/coloradoavalanche', 'Colorado', 'Avalanche'],
                      'NSH': ['/r/predators', 'Nashville', 'Predators'], 'CHI': ['/r/hawks', 'Chicago', 'Blackhawks'],
                      'NJD': ['/r/devils', 'New Jersey', 'Devils'], 'DAL': ['/r/dallasstars', 'Dallas', 'Stars'],
                      'CGY': ['/r/calgaryflames', 'Calgary', 'Flames'], 'NYR': ['/r/rangers', 'New York', 'Rangers'],
                      'CAR': ['/r/canes', 'Carolina', 'Hurricanes'], 'WPG': ['/r/winnipegjets', 'Winnipeg', 'Jets'],
                      'BUF': ['/r/sabres', 'Buffalo', 'Sabres'], 'VAN': ['/r/canucks', 'Vancouver', 'Canucks'],
                      'STL': ['/r/stlouisblues', 'St Louis', 'Blues'],
                      'SJS': ['/r/sanjosesharks', 'San Jose', 'Sharks'], 'MTL': ['/r/habs', 'Montreal', 'Canadiens'],
                      'PHI': ['/r/flyers', 'Philadelphia', 'Flyers'], 'ANA': ['/r/anaheimducks', 'Anaheim', 'Ducks'],
                      'LAK': ['/r/losangeleskings', 'Los Angeles', 'Kings'],
                      'CBJ': ['/r/bluejackets', 'Columbus', 'Blue Jackets'],
                      'PIT': ['/r/penguins', 'Pittsburgh', 'Penguins'],
                      'EDM': ['/r/edmontonoilers', 'Edmonton', 'Oilers'],
                      'TBL': ['/r/tampabaylightning', 'Tampa Bay', 'Lightning'],
                      'ARI': ['/r/coyotes', 'Arizona', 'Coyotes'], 'OTT': ['/r/ottawasenators', 'Ottawa', 'Senators']}
        self.convert = {'Vegas Golden Knights': 'VGK', 'San Jose Sharks': 'SJS', 'Detroit Red Wings': 'DET',
                        'Arizona Coyotes': 'ARI', 'Carolina Hurricanes': 'CAR', 'Toronto Maple Leafs': 'TOR',
                        'Boston Bruins': 'BOS', 'Florida Panthers': 'FLA', 'Columbus Blue Jackets': 'CBJ',
                        'Anaheim Ducks': 'ANA', 'Buffalo Sabres': 'BUF', 'Montreal Canadiens': 'MTL',
                        'Edmonton Oilers': 'EDM', 'Pittsburgh Penguins': 'PIT', 'New York Rangers': 'NYR',
                        'Washington Capitals': 'WSH', 'St Louis Blues': 'STL', 'Colorado Avalanche': 'COL',
                        'Minnesota Wild': 'MIN', 'Dallas Stars': 'DAL', 'Winnipeg Jets': 'WPG',
                        'New Jersey Devils': 'NJD', 'Tampa Bay Lightning': 'TBL', 'Los Angeles Kings': 'LAK',
                        'Calgary Flames': 'CGY', 'Chicago Blackhawks': 'CHI', 'New York Islanders': 'NYI',
                        'Nashville Predators': 'NSH', 'Ottawa Senators': 'OTT', 'Vancouver Canucks': 'VAN',
                        'Philadelphia Flyers': 'PHI'}
        self.colors = {'ANA': ['#F47A38', '#B09862', '#C4CED4', '#010101'], 'ARI': ['#8C2633', '#E2D6B5', '#111111'],
                       'BOS': ['#FFB81C', '#000000'], 'BUF': ['#002654', '#FCB514', '#ADAFAA'],
                       'CGY': ['#C8102E', '#F1BE48', '#111111'], 'CAR': ['#CC0000', '#000000', '#A2AAAD', '#76232F'],
                       'CHI': ['#CF0A2C', '#000000', '#D18A00', '#FFD100', '#00833E', '#FF671B', '#001970'],
                       'COL': ['#6F263D', '#236192', '#A2AAAD', '#000000'], 'CBJ': ['#002654', '#CE1126', '#A4A9AD'],
                       'DAL': ['#006847', '#8F8F8C', '#111111'], 'DET': ['#CE1126'], 'EDM': ['#041E42', '#FF4C00'],
                       'FLA': ['#041E42', '#C8102E', '#B9975B'], 'LAK': ['#111111', '#A2AAAD'],
                       'MIN': ['#154734', '#A6192E', '#EAAA00', '#DDCBA4'], 'MTL': ['#AF1E2D', '#192168'],
                       'NSH': ['#FFB81C', '#041E42'], 'NJD': ['#CE1126', '#000000'], 'NYI': ['#00539B', '#F47D30'],
                       'NYR': ['#0038A8', '#CE1126'], 'OTT': ['#E31837', '#C69214', '#000000'],
                       'PHI': ['#F74902', '#000000'], 'PIT': ['#000000', '#CFC493', '#FCB514'],
                       'STL': ['#002F87', '#FCB514', '#041E42'], 'SJS': ['#006D75', '#EA7200', '#000000'],
                       'TBL': ['#002868'], 'TOR': ['#003E7E'], 'VAN': ['#001F5B', '#00843D', '#071C2C', '#99999A'],
                       'VGK': ['#B4975A', '#333F42', '#C8102E', '#000000'], 'WSH': ['#041E42', '#C8102E'],
                       'WPG': ['#041E42', '#004C97', '#AC162C', '#7B303E', '#55565A', '#8E9090']}

        self.utc = pytz.timezone('UTC')
        self.pacific = pytz.timezone('US/Pacific')
        self.mountain = pytz.timezone('US/Mountain')
        self.central = pytz.timezone('US/Central')
        self.eastern = pytz.timezone('US/Eastern')
        self.atlantic = pytz.timezone('Canada/Atlantic')
 
        self.gameThread = {}
        self.subreddit = 'hockey'
        self.final = False
        self.cstats = False  # turns chatter stats on
        self.gdt = True  # update GDT or not
        self.hockeygt = False  # use /r/hockeygt to generate GDT
        self.r = r
        self.imgur = imgur
        self.data = {}
        self.excluded = []  # excluded comment ids
        self.heavy = heavy
 
    def scrape_games(self):

        today = datetime.now(self.pacific).strftime('%Y-%m-%d')
        url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + today + '&endDate=' + today + \
            '&expand=schedule.teams,schedule.linescore,schedule.broadcasts'
        w = requests.get(url)
        data = json.loads(w.content.decode('utf-8'))['dates'][0]['games']
        w.close()
 
        games = {}
        z = 1
        for x in data[:]:
            if 'broadcasts' in x:
                bcast = [item['name'] for item in x['broadcasts']]
            else:
                bcast = []
            games[z] = {'a': x['teams']['away']['team']['abbreviation'],
                        'h': x['teams']['home']['team']['abbreviation'], 'id': x['gamePk'], 'broadcasts': bcast}
            if x['linescore']['currentPeriod'] == 0:
                games[z]['time'] = 'Pre-game'
            elif x['linescore']['currentPeriodTimeRemaining'] == 'Final':
                games[z]['time'] = 'Finished'
            else:
                games[z]['time'] = x['linescore']['currentPeriodOrdinal'] + ' ' + \
                                   x['linescore']['currentPeriodTimeRemaining']
            z += 1
 
        for x in sorted(games.keys()):
            print('{0}. {1} at {2} - {3}'.format(x, games[x]['a'], games[x]['h'], games[x]['time']))
 
        response = input('Please enter the number of the game you need: ')
        valid = False
        while not valid:
            try:
                self.gameThread = games[int(response)]
            except Exception as e:
                response = input('Invalid input, please enter the number of the game you need: ')
            else:
                valid = True
 
    def find_gdt(self):
        search = input('Have you already posted the GDT? (y/n) ')
        if search.lower() == 'y':

            subcheck = input('In /r/hockey? (y/n) ')
            if subcheck.lower() == 'y':
                self.subreddit = 'hockey'
            else:
                self.subreddit = input('Which subreddit? ').lower()

            user = self.r.redditor(self.r.user.me().name)
            posts = [x for x in user.submissions.new(limit=100)]
 
            game_check = {}
            for x in posts[:]:
                made = self.utc.localize(datetime.utcfromtimestamp(x.created_utc)).astimezone(self.pacific)
                if (made.strftime('%d%m%Y') == datetime.now(self.pacific).strftime('%d%m%Y')) and (x.subreddit.display_name.lower() == self.subreddit):
                    team_lst = [self.teams[self.gameThread['a']][1],self.teams[self.gameThread['a']][2],self.teams[self.gameThread['h']][1],self.teams[self.gameThread['h']][2]]
                    check = sum(bool(y) for y in [team_lst[0].lower() in x.title.lower(), team_lst[1].lower() in x.title.lower(), team_lst[2].lower() in x.title.lower(), team_lst[3].lower() in x.title.lower()])
                    if check > 0:
                        game_check[x] = check
            print('Game Check:')
            print(game_check)
            game_check_sorted = sorted(game_check.items(), key=lambda x: x[1], reverse=True)
            if len(game_check_sorted) == 0:
                search = 'n'
                print('GDT not found.')
                print(search)
            else:
                self.gameThread['thread'] = game_check_sorted[0][0]
                print('GDT found: '+self.gameThread['thread'].title)
        if search.lower() == 'n':
            gen = input('Should I generate one? (y/n) ')
            if gen.lower() == 'y':
                subcheck = input('In /r/hockey? (y/n) ')
                if subcheck.lower() == 'y':
                    self.subreddit = 'hockey'
                else:
                    self.subreddit = input('Which subreddit? ').lower()
                found = False
                if self.hockeygt:
                    for x in self.r.subreddit('hockeygt').new(limit=100):
                        made = self.utc.localize(datetime.utcfromtimestamp(x.created_utc)).astimezone(self.pacific)
                        if (made.strftime('%d%m%Y') == datetime.now(self.pacific).strftime('%d%m%Y')) and \
                                'Daily GDT Templates' in x.title:
                            sub = x
                            found = True
                    if found:
                        game_check = {}
                        all_comments = sub.comments.list()
                        for com in all_comments:
                            team_lst = [self.teams[self.gameThread['a']][1], self.teams[self.gameThread['a']][2],
                                        self.teams[self.gameThread['h']][1], self.teams[self.gameThread['h']][2]]
                            check = sum(bool(y) for y in
                                        [team_lst[0].lower() in com.body.lower(),
                                         team_lst[1].lower() in com.body.lower(),
                                         team_lst[2].lower() in com.body.lower(),
                                         team_lst[3].lower() in com.body.lower()])
                            if check > 0:
                                game_check[com] = check
                        game_check_sorted = sorted(game_check.items(), key=lambda com: com[1], reverse=True)
                        com = game_check_sorted[0][0]
                        s = com.body
                        comWT = '[Comment with all tables]()'
                        start = 'Post title: '
                        end = '\n\n ***'
                        title = s[s.find(start) + len(start):s.rfind(end)]
                        start = '**POST BODY STARTS HERE**\n\n'
                        end = comWT
                        body1 = s[s.find(start) + len(start):s.rfind(end)]
                        start = comWT
                        if self.subreddit == 'hawks':
                            end = '##Thread notes:'
                            tnotes = "##Thread Notes:\n\n" \
                                     "##Keep it civil, and be excellent to each other!\n\n" \
                                     "---\n\n" \
                                     "## Player of the Year\n\n" \
                                     "## [PTY Link](https://docs.google.com/forms/d/e/1FAIpQLSen-bwBe-" \
                                     "gxpuTeakT2D2nwAUpcVlKaWBLg4BC2w2cqeIHzsg/closedform)\n\n" \
                                     "----\n\n" \
                                     "#Discord Server Info\n\n" \
                                     "##[Click here](https://discord.gg/wxBSRH7) to join our new /r/hawks Discord " \
                                     "server\n\n" \
                                     "---\n\n" \
                                     "### LET'S GO HAWKS! [](/#TommyHawk)"
                        else:
                            end = '\n\n***\n\n**COMMENT BODY BEGINS HERE**'
                            tnotes = ''
                        body2 = s[s.find(start) + len(start):s.rfind(end)]
                        start = '**COMMENT BODY BEGINS HERE**\n\n'
                        comment = s[s.find(start) + len(start):]
                else:
                    url = 'https://statsapi.web.nhl.com/api/v1/game/' + str(self.gameThread['id']) + '/feed/live'
                    w = requests.get(url)
                    data = json.loads(w.content.decode('utf-8'))
                    w.close()
                    time = data['gameData']['datetime']['dateTime']
                    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
                    tdiff = time - datetime.now(self.utc).replace(tzinfo=None)
                    while (self.subreddit == 'hockey' or self.subreddit == 'hockeygtt') and \
                            tdiff > timedelta(hours=1, minutes=30):
                        print('Waiting... ' + str(tdiff) + ' until gametime.\n\n')
                        sleep(60)
                        tdiff = time - datetime.now(self.utc).replace(tzinfo=None)
                    print('Generating GDT...')
                    location = data['gameData']['venue']['name']
                    aID = data['gameData']['teams']['away']['id']
                    aName = data['gameData']['teams']['away']['name']
                    hID = data['gameData']['teams']['home']['id']
                    hName = data['gameData']['teams']['home']['name']
                    tzone = data['gameData']['teams']['home']['venue']['timeZone']
                    atzone = data['gameData']['teams']['away']['venue']['timeZone']
                    url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(aID) + '/stats'
                    w = requests.get(url)
                    adata = json.loads(w.content.decode('utf-8'))
                    w.close()
                    url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(hID) + '/stats'
                    w = requests.get(url)
                    hdata = json.loads(w.content.decode('utf-8'))
                    w.close()
                    astats = adata['stats'][0]['splits'][0]['stat']
                    arec = str(astats['wins']) + '-' + str(astats['losses']) + '-' + str(astats['ot'])
                    hstats = hdata['stats'][0]['splits'][0]['stat']
                    hrec = str(hstats['wins']) + '-' + str(hstats['losses']) + '-' + str(hstats['ot'])
# Title
                    title = 'Game Thread: ' + aName + ' (' + arec + ') at ' + hName + ' (' + hrec + ') - ' + \
                        self.utc.localize(time).astimezone(pytz.timezone(tzone['id'])).strftime('%d %b %Y') + ' - ' +\
                        self.utc.localize(time).astimezone(pytz.timezone(tzone['id'])).strftime('%I:%M%p') + ' ' +\
                        tzone['tz']
                    ared = '[' + self.gameThread['a'] + '](' + self.teams[self.gameThread['a']][0] + ')'
                    hred = '[' + self.gameThread['h'] + '](' + self.teams[self.gameThread['h']][0] + ')'
                    aredl = '[' + self.teams[self.gameThread['a']][2] + '](' + self.teams[self.gameThread['a']][0] + ')'
                    hredl = '[' + self.teams[self.gameThread['h']][2] + '](' + self.teams[self.gameThread['h']][0] + ')'
# Body
                    body1 = '#' + self.teams[self.gameThread['a']][1] + ' [](' + self.teams[self.gameThread['a']][0] +\
                        ') ' + self.teams[self.gameThread['a']][2] + ' (' + arec + ') at ' +\
                        self.teams[self.gameThread['h']][1] + ' [](' + self.teams[self.gameThread['h']][0] +\
                        ') ' + self.teams[self.gameThread['h']][2] + ' (' + hrec + ')\n\n#' + location + '\n\n'
                    comWT = comWT = '[Comment with all tables]()'
                    body2 = '\n\n#In-Game Updates\n\n***\n\n***\n\n#Time\n\n|PT|MT|CT|ET|AT|\n|:--:|:--:|:--:|:--:|:--:|' +\
                        '\n|' + self.utc.localize(time).astimezone(self.pacific).strftime('%I:%M%p') + '|' +\
                        self.utc.localize(time).astimezone(self.mountain).strftime('%I:%M%p') + '|' + \
                        self.utc.localize(time).astimezone(self.central).strftime('%I:%M%p') + '|' + \
                        self.utc.localize(time).astimezone(self.eastern).strftime('%I:%M%p') + '|' + \
                        self.utc.localize(time).astimezone(self.atlantic).strftime('%I:%M%p') + '|\n\n' + \
                        '##Watch, Listen and Talk:\n\n|||\n|:--:|:--:|\n|TV|' +\
                        ", ".join(self.gameThread['broadcasts']) + '|\n|Streams|First Row - ATDHE - Vipbox - '+\
                        'StreamHunter - LiveTV - /r/nhlstreams - /r/puckstreams|\n' + \
                        '| Listen | [' + self.gameThread['a'] + '](https://www.nhl.com/video/c-0009991' + str(aID) + \
                        ') - [' + self.gameThread['h'] + '](https://www.nhl.com/video/c-0009991' + str(hID) +\
                        ')|\n| Other |[Preview](' + 'http://www.nhl.com/gamecenter/en/preview?id=' +\
                        str(self.gameThread['id']) + ') - ' +\
                        '[Boxscore](http://www.nhl.com/gamecenter/en/boxscore?id=' + str(self.gameThread['id']) +\
                        ') - [Recap](http://www.nhl.com/gamecenter/en/recap?id=' + str(self.gameThread['id']) + ')|' +\
                        '\n|GameCenter|[On NHL.com](https://www.nhl.com/gamecenter/' + str(self.gameThread['id']) +\
                        ')|\n\n'
# Thread Notes
                    if self.subreddit == 'hawks':
                        tnotes = "##Thread Notes:\n\n" \
                                 "##Keep it civil, and be excellent to each other!\n\n" \
                                 "---\n\n" \
                                 "## Player of the Year\n\n" \
                                 "## [PTY Link](https://docs.google.com/forms/d/e/1FAIpQLSen-bwBe-" \
                                 "gxpuTeakT2D2nwAUpcVlKaWBLg4BC2w2cqeIHzsg/closedform)\n\n" \
                                 "----\n\n" \
                                 "#Discord Server Info\n\n" \
                                 "##[Click here](https://discord.gg/wxBSRH7) to join our new /r/hawks Discord " \
                                 "server\n\n" \
                                 "---\n\n" \
                                 "### LET'S GO HAWKS! [](/#TommyHawk)"
                    else:
                        tnotes = '##Thread Notes:\n\n* Keep it civil\n\n* Sort by new for best results\n\n' +\
                            '##Subscribe:\n\n###' + aredl + ' and ' + hredl + '.'
# Comment tables
                    url = 'https://statsapi.web.nhl.com/api/v1/game/' + str(self.gameThread['id']) + '/content'
                    w = requests.get(url)
                    pdata = json.loads(w.content.decode('utf-8'))
                    w.close()
# Projected Lineup
                    if len(pdata['editorial']['preview']['items']) > 0:
                        url = 'https://www.nhl.com' + pdata['editorial']['preview']['items'][0]['url']
                        w = requests.get(url)
                        h = html2text.HTML2Text()
                        h.ignore_links = True
                        s = h.handle(w.text)
                        s = s.replace("\\", "")
                        s = s.replace("_", "")
                        s = s.replace("#####", "###")
                        s = s.replace(" ** ", "**")
                        s = s.replace("Maple Leafs", "Leafs")
                        s = s.replace(self.teams[self.gameThread['a']][2], aredl)
                        s = s.replace(self.teams[self.gameThread['h']][2], hredl)
                        start = '###  **' + aredl + ' projected lineup**'
                        end = '###  **Status report**'
                        projlineup = s[s.find(start):s.rfind(end)]
                    else:
                        print("Couldn't find lineup. Looking in /r/hockeygt...")
                        for x in self.r.subreddit('hockeygt').new(limit=100):
                            made = self.utc.localize(datetime.utcfromtimestamp(x.created_utc)).astimezone(self.pacific)
                            if (made.strftime('%d%m%Y') == datetime.now(self.pacific).strftime('%d%m%Y')) and \
                                    'Daily GDT Templates' in x.title:
                                sub = x
                                found = True
                        if found:
                            game_check = {}
                            all_comments = sub.comments.list()
                            for com in all_comments:
                                team_lst = [self.teams[self.gameThread['a']][1], self.teams[self.gameThread['a']][2],
                                            self.teams[self.gameThread['h']][1], self.teams[self.gameThread['h']][2]]
                                check = sum(bool(y) for y in
                                            [team_lst[0].lower() in com.body.lower(),
                                             team_lst[1].lower() in com.body.lower(),
                                             team_lst[2].lower() in com.body.lower(),
                                             team_lst[3].lower() in com.body.lower()])
                                if check > 0:
                                    game_check[com] = check
                            game_check_sorted = sorted(game_check.items(), key=lambda com: com[1], reverse=True)
                            com = game_check_sorted[0][0]
                            s = com.body
                            start = '**COMMENT BODY BEGINS HERE**\n\n'
                            end = '###Team Stats'
                            projlineup = s[s.find(start) + len(start):s.rfind(end)]
# Team Stats
                    teamstats = '###Team Stats\n\n|Team|GP|W|L|OT|P|P%|G/G|GA/G|PP%|PK%|S/G|SA/G|FO%|\n' +\
                        '|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n' +\
                        '|' + aredl + '|' + str(astats['gamesPlayed']) + '|' + str(astats['wins']) + '|' +\
                        str(astats['losses']) + '|' + str(astats['ot']) + '|' + str(astats['pts']) + '|' + \
                        str(astats['ptPctg']) + '|' + str(astats['goalsPerGame']) + '|' + \
                        str(astats['goalsAgainstPerGame']) + '|' + str(astats['powerPlayPercentage']) + '|' +\
                        str(astats['penaltyKillPercentage']) + '|' + str(astats['shotsPerGame']) + '|' +\
                        str(astats['shotsAllowed']) + '|' + str(astats['faceOffWinPercentage']) + '|\n' +\
                        '|' + hredl + '|' + str(hstats['gamesPlayed']) + '|' + str(hstats['wins']) + '|' +\
                        str(hstats['losses']) + '|' + str(hstats['ot']) + '|' + str(hstats['pts']) + '|' +\
                        str(hstats['ptPctg']) + '|' + str(hstats['goalsPerGame']) + '|' +\
                        str(hstats['goalsAgainstPerGame']) + '|' + str(hstats['powerPlayPercentage']) + '|' +\
                        str(hstats['penaltyKillPercentage']) + '|' + str(hstats['shotsPerGame']) + '|' +\
                        str(hstats['shotsAllowed']) + '|' + str(hstats['faceOffWinPercentage']) + '|\n\n'
# Goalies
                    ascorers = []
                    askaters = []
                    hscorers = []
                    hskaters = []
                    apos = []
                    hpos = []
                    goalies = '### Goalie Breakdown\n\n||Name|GP|GS|W|L|OT|SO|GAA|SV%|\n' +\
                              '|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n'
                    url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(aID) + '?expand=team.roster'
                    w = requests.get(url)
                    adata = json.loads(w.content.decode('utf-8'))
                    w.close()
                    for player in adata['teams'][0]['roster']['roster']:
                        url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(player['person']['id']) + \
                              '/stats/?stats=statsSingleSeason'
                        w = requests.get(url)
                        pstats = json.loads(w.content.decode('utf-8'))
                        w.close()
                        if len(pstats['stats'][0]['splits']) != 0:
                            if player['position']['code'] == 'G':
                                gstats = pstats['stats'][0]['splits'][0]['stat']
                                goalies += '|' + ared + '|' + player['person']['fullName'] + '|' + str(gstats['games']) +\
                                    '|' + str(gstats['gamesStarted']) + '|' + str(gstats['wins']) +'|' +\
                                    str(gstats['losses']) + '|' + str(gstats['ot']) + '|' + str(gstats['shutouts']) +\
                                    '|' + str(gstats['goalAgainstAverage']) + '|' + str(gstats['savePercentage']) + '|\n'
                            elif pstats['stats'][0]['splits'][0]['stat']['points'] > 0:
                                sstats = pstats['stats'][0]['splits'][0]['stat']
                                ascorers.append(sstats)
                                askaters.append(player['person']['fullName'])
                                apos.append(player['position']['abbreviation'])
                    goalies += '|--|--|--|--|--|--|--|--|--|--|\n'
                    url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(hID) + '?expand=team.roster'
                    w = requests.get(url)
                    hdata = json.loads(w.content.decode('utf-8'))
                    w.close()
                    for player in hdata['teams'][0]['roster']['roster']:
                        url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(player['person']['id']) + \
                              '/stats/?stats=statsSingleSeason'
                        w = requests.get(url)
                        pstats = json.loads(w.content.decode('utf-8'))
                        w.close()
                        if len(pstats['stats'][0]['splits']) != 0:
                            if player['position']['code'] == 'G':
                                gstats = pstats['stats'][0]['splits'][0]['stat']
                                goalies += '|' + hred + '|' + player['person']['fullName'] + '|' + str(gstats['games']) +\
                                    '|' + str(gstats['gamesStarted']) + '|' + str(gstats['wins']) + '|' +\
                                    str(gstats['losses']) + '|' + str(gstats['ot']) + '|' + str(gstats['shutouts']) +\
                                    '|' + str(gstats['goalAgainstAverage']) + '|' + str(gstats['savePercentage']) + '|\n'
                            elif pstats['stats'][0]['splits'][0]['stat']['points'] > 0:
                                sstats = pstats['stats'][0]['splits'][0]['stat']
                                hscorers.append(sstats)
                                hskaters.append(player['person']['fullName'])
                                hpos.append(player['position']['abbreviation'])
                    goalies += '\n'
# Top Scorers
                    tscorers = '### Top Scorers\n\n||Name|Pos|GP|G|A|Pts|+/-|PIM|S|S%|ATOI|FO%|\n' +\
                               '|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n'
                    ascorers = pd.DataFrame(ascorers, index=askaters)
                    hscorers = pd.DataFrame(hscorers, index=hskaters)
                    ascorers['pos'] = pd.Series(apos, index=ascorers.index)
                    hscorers['pos'] = pd.Series(hpos, index=hscorers.index)
                    ascorers = ascorers.sort_values(by=['points', 'goals', 'games'], ascending=[False, False, True])
                    hscorers = hscorers.sort_values(by=['points', 'goals', 'games'], ascending=[False, False, True])
                    nscorers = 5
                    for i in range(0, nscorers):
                        if i < len(ascorers.index):
                            player = ascorers.index[i]
                            tscorers += '|' + ared + '|' + player + '|' + ascorers['pos'][player] + '|' + \
                                        str(ascorers['games'][player]) + '|' + str(ascorers['goals'][player]) + '|' + \
                                        str(ascorers['assists'][player]) + '|' + str(ascorers['points'][player]) + \
                                        '|' + str(ascorers['plusMinus'][player]) + '|' + \
                                        str(ascorers['penaltyMinutes'][player]) + '|' + \
                                        str(ascorers['shots'][player]) + '|' + str(ascorers['shotPct'][player]) + \
                                        '|' + ascorers['timeOnIcePerGame'][player] + '|' + \
                                        str(ascorers['faceOffPct'][player]) + '|\n'
                    tscorers += '|--|--|--|--|--|--|--|--|--|--|--|--|--|\n'
                    for i in range(0, nscorers):
                        if i < len(ascorers.index):
                            player = hscorers.index[i]
                            tscorers += '|' + hred + '|' + player + '|' + hscorers['pos'][player] + '|' + \
                                        str(hscorers['games'][player]) + '|' + str(hscorers['goals'][player]) + '|' + \
                                        str(hscorers['assists'][player]) + '|' + str(hscorers['points'][player]) +\
                                        '|' + str(hscorers['plusMinus'][player]) + '|' + \
                                        str(hscorers['penaltyMinutes'][player]) + '|' + \
                                        str(hscorers['shots'][player]) + '|' + str(hscorers['shotPct'][player]) + \
                                        '|' + hscorers['timeOnIcePerGame'][player] + '|' + \
                                        str(hscorers['faceOffPct'][player]) + '|\n'
                    tscorers += '\n'
# Season Series
                    seasonseries = '###Season Series\n\n|Date|Away|Home|Time|Network/Result|\n' +\
                                   '|:--:|:--:|:--:|:--:|:--:|\n'
                    url = 'https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(hID) +\
                          '&expand=schedule.broadcasts&season=' + data['gameData']['game']['season']
                    w = requests.get(url)
                    hdata = json.loads(w.content.decode('utf-8'))
                    w.close()
                    for date in hdata['dates']:
                        if (date['games'][0]['teams']['away']['team']['id'] == aID or
                                date['games'][0]['teams']['home']['team']['id'] == aID):
                            time = date['games'][0]['gameDate']
                            time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
                            if date['games'][0]['teams']['away']['team']['id'] == aID:
                                time = self.utc.localize(time).astimezone(pytz.timezone(tzone['id']))
                                seasonseries += '|' + time.strftime('%d %b %Y') + '|' + ared + '|' + hred +\
                                                '|' + time.strftime('%I:%M%p') + ' ' + tzone['tz'] + '|'
                                if date['games'][0]['status']['detailedState'] == 'Final':
                                    url = 'https://statsapi.web.nhl.com/api/v1/game/' + \
                                          str(date['games'][0]['gamePk']) + '/content'
                                    w = requests.get(url)
                                    gdata = json.loads(w.content.decode('utf-8'))
                                    w.close()
                                    ordinal = ''
                                    for milestone in gdata['media']['milestones']['items']:
                                        if milestone['ordinalNum'] == 'SO':
                                            ordinal = ' SO'
                                        elif milestone['ordinalNum'] == 'OT' and ordinal == '':
                                            ordinal = ' OT'
                                    seasonseries += self.gameThread['a'] + ' (' +\
                                                        str(date['games'][0]['teams']['away']['score']) + ') - ' +\
                                                        self.gameThread['h'] + ' (' +\
                                                        str(date['games'][0]['teams']['home']['score']) + ')' + \
                                                        ordinal + '|\n'
                                else:
                                    if 'broadcasts' in date['games'][0]:
                                        bcast = [item['name'] for item in date['games'][0]['broadcasts']]
                                    else:
                                        bcast = []
                                    seasonseries += ", ".join(bcast) + '|\n'
                            else:
                                time = self.utc.localize(time).astimezone(pytz.timezone(atzone['id']))
                                seasonseries += '|' + time.strftime('%d %b %Y') + '|' + hred + '|' + ared + \
                                                '|' + time.strftime('%I:%M%p') + ' ' + atzone['tz'] + '|'
                                if date['games'][0]['status']['detailedState'] == 'Final':
                                    url = 'https://statsapi.web.nhl.com/api/v1/game/' + \
                                          str(date['games'][0]['gamePk']) + '/content'
                                    w = requests.get(url)
                                    gdata = json.loads(w.content.decode('utf-8'))
                                    w.close()
                                    ordinal = ''
                                    for milestone in gdata['media']['milestones']['items']:
                                        if milestone['ordinalNum'] == 'SO':
                                            ordinal = ' SO'
                                        elif milestone['ordinalNum'] == 'OT' and ordinal == '':
                                            ordinal = ' OT'
                                    seasonseries += self.gameThread['h'] + ' (' + \
                                                        str(date['games'][0]['teams']['away']['score']) + ') - ' + \
                                                        self.gameThread['a'] + ' (' + \
                                                        str(date['games'][0]['teams']['home']['score']) + ')' + \
                                                        ordinal + '|\n'
                                else:
                                    if 'broadcasts' in date['games'][0]:
                                        bcast = [item['name'] for item in date['games'][0]['broadcasts']]
                                    else:
                                        bcast = []
                                    seasonseries += ", ".join(bcast) + '|\n'
                    comment = projlineup + teamstats + tscorers + goalies + seasonseries
                    found = True
                if found:
                    body = body1 + comWT + body2 + tnotes
                    sub = self.r.subreddit(self.subreddit).submit(title, selftext=body, send_replies=False)
                    com = sub.reply(comment)
                    comWT = '[Comment with all tables](' + com.permalink + ')'
                    self.excluded.append(com.id)
                    body = body1 + comWT + body2 + tnotes
                    sub.edit(body)
                    self.gameThread['thread'] = sub
                else:
                    print('GDT not found.')
                    thread = input('GDT URL? ')
                    self.gameThread['thread'] = self.r.submission(url=thread)
            else:
                gen = input('Chatter stats only? (y/n) ')
                if gen.lower() == 'y':
                    self.cstats = True
                    self.gdt = False
                    subcheck = input('In /r/hockey? (y/n) ')
                    if subcheck.lower() == 'y':
                        self.subreddit = 'hockey'
                    else:
                        self.subreddit = input('Which subreddit? ').lower()
                    posts = [x for x in self.r.subreddit(self.subreddit).new(limit=100)]

                    game_check = {}
                    for x in posts[:]:
                        made = self.utc.localize(datetime.utcfromtimestamp(x.created_utc)).astimezone(self.pacific)
                        if (made.strftime('%d%m%Y') == datetime.now(self.pacific).strftime('%d%m%Y')) and (
                                x.subreddit.display_name.lower() == self.subreddit):
                            team_lst = [self.teams[self.gameThread['a']][1], self.teams[self.gameThread['a']][2],
                                        self.teams[self.gameThread['h']][1], self.teams[self.gameThread['h']][2]]
                            check = sum(bool(y) for y in
                                        [team_lst[0].lower() in x.title.lower(), team_lst[1].lower() in x.title.lower(),
                                         team_lst[2].lower() in x.title.lower(),
                                         team_lst[3].lower() in x.title.lower()])
                            if check > 0:
                                game_check[x] = check
                    print('Game Check:')
                    print(game_check)
                    game_check_sorted = sorted(game_check.items(), key=lambda x: x[1], reverse=True)
                    if len(game_check_sorted) == 0:
                        print('GDT not found.')
                        thread = input('GDT URL? ')
                        self.gameThread['thread'] = self.r.submission(url=thread)
                    else:
                        self.gameThread['thread'] = game_check_sorted[0][0]
                        print('GDT found: ' + self.gameThread['thread'].title)
                else:
                    thread = input('GDT URL? ')
                    self.gameThread['thread'] = self.r.submission(url=thread)
        #csbool = input('Chatter Stats? (y/n) ')
        #if csbool.lower() == 'y':
        #    self.cstats = True

    def color_fun(self, word, font_size, position, orientation, random_state=None, **kwargs):
        rn = r.randint(0, 2)
        if rn == 0:
            if 'gameData' in self.data.keys():
                t = self.data['gameData']['teams']['away']['abbreviation']
            else:
                t = self.data['teams']['away']['team']['abbreviation']
        else:
            if 'gameData' in self.data.keys():
                t = self.data['gameData']['teams']['home']['abbreviation']
            else:
                t = self.data['teams']['home']['team']['abbreviation']
        colpal = self.colors[t]
        p = np.array(range(0, len(colpal)), dtype=float)
        p = np.power(2, -p)
        p = p/np.sum(p)
        return np.random.choice(colpal, p=p)


# Chatter Stats
    def chatter_stats(self, data, thread):

        self.data = data

        if 'liveData' in data.keys():
            time = data['liveData']['linescore']['currentPeriodTimeRemaining']
            period = data['liveData']['linescore']['currentPeriod']
        elif 'linescore' in data.keys():
            time = data['linescore']['currentPeriodTimeRemaining']
            period = data['linescore']['currentPeriod']
        else:
            raise Exception('Chatter stats cannot find line score.')

        if 'gameData' in data.keys():
            gtype = data['gameData']['game']['type']
        elif 'gameType' in data.keys():
            gtype = data['gameType']
        else:
            raise Exception('Chatter stats cannot find game type.')

        if self.cstats and (time == 'Final' or (('END' in time) and (gtype == 'P' or period < 3 or time == 'Final'))
                            or self.heavy):

            if time == 'Final':
                cflag = 'Final'
            elif 'END' in time:
                if period > 3:
                    cflag = ordinal(period - 3) + ' OT'
                else:
                    cflag = ordinal(period)
                cflag = 'End of ' + cflag
            else:
                cflag = ''
            try:
                print('Creating chatterstats...')

                # get submission text
                sub = self.r.submission(id=thread)
                text = sub.selftext
                text = text.replace(')', ' ')
                text = text.replace('(', ' ')
                urls = re.findall(r'http\S+', text.lower())
                redurl = 'http://www.reddit.com'
                rurls = re.findall(r'/r/\S+', text.lower())
                urls.extend([redurl + s for s in rurls])
                rurls = [s for s in urls if 'reddit' in s]

                for url in rurls:
                    try:
                        com = self.r.comment(url=url)
                        if com.id not in self.excluded:
                            self.excluded.append(com.id)
                    except Exception as e:
                        pass
                print(self.excluded)

                # get comments
                sub.comments.replace_more(limit=None)
                all_comments = sub.comments.list()

                # initialize
                authors = []
                flair = []
                aCts = []
                potty = []
                words = []
                remove_digits = str.maketrans('', '', digits)

                # swear words
                sWords = ['fuck', 'fucking', 'shit', 'shitty', 'damn', 'damnit', 'bitch', 'bitching', 'ass', 'fuckers',
                          'shat', 'crap', 'cunt', 'shite', 'fuckin', 'bullshit', 'fucks']
                for com in all_comments:
                    auth = com.author
                    if (auth is not None) and (com.id not in self.excluded):

                        # clean text
                        text = ''.join(com.body)
                        text = text.translate(remove_digits)
                        text = re.sub(r'http\S+', '', text.lower())
                        text = re.sub(r'/r/\S+', '', text.lower())
                        body = re.findall(r"[\w']+", text)

                        # find swear words
                        swears = [item for item in body if item in sWords]
                        pWords = len(swears)

                        # check if new or old author
                        if auth.name not in authors:
                            authors.append(auth.name)
                            aCts.append(1)
                            fl = com.author_flair_text
                            if fl is None:
                                fl = 'None'
                            flair.append(fl)
                            potty.append(pWords)
                        else:
                            ind = authors.index(auth.name)
                            aCts[ind] += 1
                            potty[ind] += pWords
                        words.extend(body)

                # create word cloud
                wc = WordCloud(
                    background_color='white',
                    stopwords=set(STOPWORDS),
                    max_words=200,
                    max_font_size=40,
                    scale=3,
                    random_state=1
                ).generate(" ".join(words))
                wc.recolor(color_func=self.color_fun, random_state=1)
                wfile = 'wordcloud_' + self.subreddit + '.png'
                wc.to_file(wfile)


                # upload to imgur
                im = pyimgur.Imgur(self.imgur)
                uploaded_image = im.upload_image(wfile, title="Chatter Stats Word Cloud")
                tnW = len(words)

                aCts = np.array(aCts)
                nC = np.sum(aCts)
                if nC > 0:
                    nA = len(authors)
                    aInd = np.argsort(-aCts)
                    pInd = np.argmax(potty)
                    (uF, fCts) = np.unique(flair, return_counts=True)
                    nhlF = [item for item in uF if ('NHL' in item and 'NHLR' not in item)]
                    nF = len(uF)
                    fInd = np.argsort(-fCts)
                    chatterstats = '#Chatterstats - ' + cflag + '\n\n'
                    if self.subreddit == 'hockey':
                        chatterstats += '|Stat|Count||Most Comments (user)|Count||Most Commenters (flair)|Count|\n' + \
                                        '|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n'
                        ctemp = [''] * 7
                        ctemp[0] = '|Number of comments|{0}|'.format(nC)
                        ctemp[1] = '|Number of unique commenters|{0}|'.format(nA)
                        ctemp[2] = '|Average comments per user|{0}|'.format(round(nC / nA, 2))
                        ctemp[3] = '|Number of unique flairs|{0}|'.format(nF)
                        ctemp[4] = '|Number of NHL teams|{0}|'.format(len(nhlF))
                        ctemp[5] = '|Average number of words per comment|{0}|'.format(round(tnW / nC, 2))
                        if potty[pInd] == 0:
                            ctemp[6] = '|Dirtiest mouth: None|0|'
                        else:
                            ctemp[6] = '|Dirtiest mouth: /u/{0}|{1}|'.format(authors[pInd], potty[pInd])
                    else:
                        chatterstats += '|Stat|Count||Most Comments (user)|Count|\n' + \
                                        '|:--:|:--:|:--:|:--:|:--:|\n'
                        ctemp = [''] * 5
                        ctemp[0] = '|Number of comments|{0}|'.format(nC)
                        ctemp[1] = '|Number of unique commenters|{0}|'.format(nA)
                        ctemp[2] = '|Average comments per user|{0}|'.format(round(nC / nA, 2))
                        ctemp[3] = '|Average number of words per comment|{0}|'.format(round(tnW / nC, 2))
                        if potty[pInd] == 0:
                            ctemp[4] = '|Dirtiest mouth: None|0|'
                        else:
                            ctemp[4] = '|Dirtiest mouth: /u/{0}|{1}|'.format(authors[pInd], potty[pInd])

                    for i in range(0, len(ctemp)):
                        if len(ctemp) > i:
                            chatterstats += ctemp[i]
                        else:
                            chatterstats += '|||'
                        if nA > i:
                            chatterstats += '|/u/{0}|{1}|'.format(authors[aInd[i]], aCts[aInd[i]])
                        else:
                            chatterstats += '|||'
                        if self.subreddit == 'hockey':
                            if nF > i:
                                chatterstats += '|{0}|{1}|\n'.format(uF[fInd[i]], fCts[fInd[i]])
                            else:
                                chatterstats += '|||\n'
                        else:
                            chatterstats += '\n'
                    chatterstats += '\n[Word Cloud](' + uploaded_image.link + ')\n\n' + \
                                    'Please refrain from spamming and/or otherwise gaming the system.\n\n' + \
                                    'This is a Beta version. Message /u/sandman730 with any bugs.\n\n'
                    com = sub.reply(chatterstats)
                    self.excluded.append(com.id)
            except Exception as e:
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
 
    def update_gdt(self):
        url = 'https://statsapi.web.nhl.com/api/v1/game/'+str(self.gameThread['id'])+'/feed/live'
        w = requests.get(url)
        data = json.loads(w.content.decode('utf-8'))
        w.close()

        url = 'https://statsapi.web.nhl.com/api/v1/game/' + str(self.gameThread['id']) + '/content'
        w = requests.get(url)
        cdata = json.loads(w.content.decode('utf-8'))
        w.close()
 
        period = data['liveData']['linescore']['currentPeriod']
        if period == 0:
            print('No updates')
            time = 'Pre-game'
        else:
            time = data['liveData']['linescore']['currentPeriodTimeRemaining']
            ordinal = data['liveData']['linescore']['currentPeriodOrdinal']
            if ordinal+' '+time == self.gameThread['time']:
                print('No updates')
            else:
                self.gameThread['time'] = ordinal+' '+time
#Time Table
                if self.gdt:
                    print('Creating time table...')
                    if time == 'Final':
                        timeTable = '|Time Clock|\n|:--:|\n|FINAL|\n\n'
                    else:
                        timeTable = '|Time Clock|\n|:--:|\n|{0} - {1}|\n\n'.format(ordinal, time)

                    homeTeam = self.teams[data['gameData']['teams']['home']['abbreviation']][0]
                    awayTeam = self.teams[data['gameData']['teams']['away']['abbreviation']][0]
                    # Boxscore
                    print('Creating boxscore...')
                    boxscore = '|Teams|1st|2nd|3rd|'

                    if data['gameData']['game']['type'] == 'R':
                        if period == 4:
                            boxscore += 'OT|Total|\n|:--:|:--:|:--:|:--:|:--:|:--:|\n'
                        elif period == 5:
                            boxscore += 'OT|SO|Total|\n|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n'
                        else:
                            boxscore += 'Total|\n|:--:|:--:|:--:|:--:|:--:|\n'
                    elif data['gameData']['game']['type'] == 'P':
                        for x in range(0, (period - 3)):
                            boxscore += 'OT{0}|'.format(x + 1)
                        boxscore += 'Total|\n|:--:|:--:|:--:|:--:|'
                        for x in range(0, period - 3):
                            boxscore += ':--:|'
                        boxscore += ':--:|\n'

                    homeTotal = data['liveData']['linescore']['teams']['home']['goals']
                    awayTotal = data['liveData']['linescore']['teams']['away']['goals']

                    scoreDict = {}

                    OT = 1
                    for x in data['liveData']['linescore']['periods']:
                        score = [x['away']['goals'], x['home']['goals']]
                        if (data['gameData']['game']['type'] == 'P') and ('OT' in x['ordinalNum']) and (period > 4):
                            scoreDict['OT' + str(OT)] = score
                            OT += 1
                        else:
                            scoreDict[x['ordinalNum']] = score

                    if period == 1:
                        scoreDict['2nd'] = ['--', '--']
                        scoreDict['3rd'] = ['--', '--']
                    elif period == 2:
                        scoreDict['3rd'] = ['--', '--']

                    if data['liveData']['linescore']['hasShootout']:
                        awaySO = data['liveData']['linescore']['shootoutInfo']['away']['scores']
                        homeSO = data['liveData']['linescore']['shootoutInfo']['home']['scores']
                        if awaySO > homeSO:
                            scoreDict['SO'] = [1, 0]
                        else:
                            scoreDict['SO'] = [0, 1]

                    boxscore += '|[]({0})|'.format(awayTeam)
                    for x in sorted(scoreDict.keys()):
                        boxscore += '{0}|'.format(scoreDict[x][0])

                    boxscore += '{0}|\n|[]({1})|'.format(awayTotal, homeTeam)
                    for x in sorted(scoreDict.keys()):
                        boxscore += '{0}|'.format(scoreDict[x][1])

                    boxscore += '{0}|\n\n'.format(homeTotal)
                    # Team Stats
                    print('Creating team stats...')
                    homeStats = data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']
                    awayStats = data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']

                    teamStats = '|Team|Shots|Hits|Blocked|FO Wins|Giveaways|Takeaways|Power Plays|\n|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n'
                    teamStats += '|[]({0})|{1}|{2}|{3}|{4}%|{5}|{6}|{7}/{8}|\n'.format(awayTeam, awayStats['shots'],
                                                                                       awayStats['hits'],
                                                                                       awayStats['blocked'], awayStats[
                                                                                           'faceOffWinPercentage'],
                                                                                       awayStats['giveaways'],
                                                                                       awayStats['takeaways'], str(
                            int(awayStats['powerPlayGoals'])), str(int(awayStats['powerPlayOpportunities'])))
                    teamStats += '|[]({0})|{1}|{2}|{3}|{4}%|{5}|{6}|{7}/{8}|\n\n'.format(homeTeam, homeStats['shots'],
                                                                                         homeStats['hits'],
                                                                                         homeStats['blocked'],
                                                                                         homeStats[
                                                                                             'faceOffWinPercentage'],
                                                                                         homeStats['giveaways'],
                                                                                         homeStats['takeaways'], str(
                            int(homeStats['powerPlayGoals'])), str(int(homeStats['powerPlayOpportunities'])))
                    # Goals
                    print('Creating goal table...')
                    allPlays = data['liveData']['plays']['allPlays']
                    scoringPlays = data['liveData']['plays']['scoringPlays']

                    goalDict = {'1st': [], '2nd': [], '3rd': [], 'OT': []}

                    if (data['gameData']['game']['type'] == 'R') and (period == 5):
                        goalDict['SO'] = []
                    if (data['gameData']['game']['type'] == 'P') and (period > 4):
                        del goalDict['OT']
                        for x in range(0, (period - 4)):
                            goalDict['OT' + str(x + 1)] = []


                    OT = 1
                    for x in scoringPlays:
                        goal = allPlays[x]
                        for y in cdata['media']['milestones']['items']:
                            if (y['title'] == 'Goal' and str(y['period']) == str(goal['about']['period']) and
                                    str(y['statsEventId']) == str(goal['about']['eventId']) and
                                    len(y['highlight']) > 0):
                                url = y['highlight']['playbacks'][-1]['url']
                                goal['result']['description'] = '[' + goal['result']['description'] + '](' + url + ')'

                        if (data['gameData']['game']['type'] == 'P') and ('OT' in goal['about']['ordinalNum']) and (
                                period > 4):
                            goalDict['OT' + str(OT)].append([goal['about']['periodTime'], self.teams[
                                self.convert[goal['team']['name'].replace(u'\xe9', 'e').replace('.', '')]][0],
                                                             goal['result']['strength']['name'],
                                                             goal['result']['description'].replace(u'\xe9', 'e')])
                            OT += 1
                        else:
                            goalDict[goal['about']['ordinalNum']].append([goal['about']['periodTime'], self.teams[
                                self.convert[goal['team']['name'].replace(u'\xe9', 'e').replace('.', '')]][0],
                                                                          goal['result']['strength']['name'],
                                                                          goal['result']['description'].replace(u'\xe9',
                                                                                                                'e')])


                    goalTable = '|Period|Time|Team|Strength|Description|\n|:--:|:--:|:--:|:--:|:--:|\n'
                    # Reverse for GDT and forward for PGT
                    for x in sorted(goalDict.keys(), reverse=True):
                        for y in goalDict[x][::-1]:
                            if x == 'SO':
                                goalTable += '|{0}|{1}|[]({2})|---|{3}|\n'.format(x, y[0], y[1], y[3])
                            else:
                                goalTable += '|{0}|{1}|[]({2})|{3}|{4}|\n'.format(x, y[0], y[1], y[2], y[3])

                    goalTable += '\n\n'
                    # Penalties
                    print('Creating penalty table...')
                    penaltyPlays = data['liveData']['plays']['penaltyPlays']

                    penaltyDict = {'1st': [], '2nd': [], '3rd': [], 'OT': []}

                    if (data['gameData']['game']['type'] == 'P') and (period > 4):
                        del penaltyDict['OT']
                        for x in range(0, (period - 4)):
                            penaltyDict['OT' + str(x + 1)] = []

                    OT = 1
                    for x in penaltyPlays:
                        penalty = allPlays[x]
                        if (data['gameData']['game']['type'] == 'P') and ('OT' in penalty['about']['ordinalNum']) and (
                                period > 4):
                            penaltyDict['OT' + str(OT)].append([penalty['about']['periodTime'], self.teams[
                                self.convert[penalty['team']['name'].replace(u'\xe9', 'e').replace('.', '')]][0],
                                                                penalty['result']['penaltySeverity'],
                                                                penalty['result']['penaltyMinutes'],
                                                                penalty['result']['description'].replace(u'\xe9', 'e')])
                        else:
                            penaltyDict[penalty['about']['ordinalNum']].append([penalty['about']['periodTime'],
                                                                                self.teams[self.convert[
                                                                                    penalty['team']['name'].replace(
                                                                                        u'\xe9', 'e').replace('.',
                                                                                                              '')]][0],
                                                                                penalty['result']['penaltySeverity'],
                                                                                penalty['result']['penaltyMinutes'],
                                                                                penalty['result'][
                                                                                    'description'].replace(u'\xe9',
                                                                                                           'e')])

                    penaltyTable = '|Period|Time|Team|Type|Min|Description|\n|:--:|:--:|:-:|:--:|:--:|:--:|\n'
                    # Reverse for GDT and forward for PGT
                    for x in sorted(penaltyDict.keys(), reverse=True):
                        for y in penaltyDict[x][::-1]:
                            penaltyTable += '|{0}|{1}|[]({2})|{3}|{4}|{5}|\n'.format(x, y[0], y[1], y[2], y[3], y[4])

                    penaltyTable += '\n\n'

                    tables = '***\n\n' + timeTable + boxscore + teamStats + goalTable + penaltyTable + '***'

                    now = datetime.now()
                    print(now.strftime('%I:%M%p') + ' - Updating thread...')
                    h = HTMLParser()
                    op = self.gameThread['thread'].selftext.split('***')
                    self.gameThread['thread'] = self.gameThread['thread'].edit(h.unescape(op[0] + tables + op[2]))
                self.chatter_stats(data, self.gameThread['thread'])
        if time == 'Final':
            self.final = True
            close = input('Game over, hit enter/return to exit.')
        else:
            print('Sleeping...\n\n')
            sleep(60)
 
    def run(self):
        try:
            self.scrape_games()
            self.find_gdt()
            while not self.final:
                self.update_gdt()
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(traceback.format_exc())


class Chatter_Stats_Bot(Auto_Updater_Bot):
    def __init__(self, r, imgur, subreddit='hockey', heavy=False):
        super().__init__(r, imgur, heavy=heavy)

        self.cstats = True
        self.games = {}
        self.scheduleURL = ''
        self.subreddit = subreddit
        self.date = datetime.now(self.pacific).strftime('%Y-%m-%d')

    def scrape_games(self):

        self.scheduleURL = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + self.date + '&endDate=' +\
                           self.date + '&expand=schedule.teams,schedule.linescore'
        w = requests.get(self.scheduleURL)
        data = json.loads(w.content.decode('utf-8'))['dates']
        w.close()

        if len(data) > 0:
            data=data[0]['games']

        z = 1
        for x in data[:]:
            aab = x['teams']['away']['team']['abbreviation']
            hab = x['teams']['home']['team']['abbreviation']
            sred = '/r/'+self.subreddit
            if self.subreddit == 'hockey' or self.subreddit == 'hockeygtt' or self.teams[aab][0] == sred \
                    or self.teams[hab][0] == sred:
                self.games[z] = {'a': aab, 'h': hab, 'id': x['gamePk']}
                if x['linescore']['currentPeriod'] == 0:
                    self.games[z]['time'] = 'Pre-game'
                elif x['linescore']['currentPeriodTimeRemaining'] == 'Final':
                    self.games[z]['time'] = 'Finished'
                else:
                    self.games[z]['time'] = x['linescore']['currentPeriodOrdinal'] + ' ' + \
                                            x['linescore']['currentPeriodTimeRemaining']
                print('{0} at {1} - {2}'.format(self.games[z]['a'], self.games[z]['h'], self.games[z]['time']))
                z += 1

    def find_gdt(self):

        posts = [x for x in self.r.subreddit(self.subreddit).new(limit=100)]

        for z in self.games:
            game = self.games[z]
            if 'thread' not in game.keys() and game['time'] != 'Pre-game' and game['time'] != 'Finished':
                game_check = {}
                for x in posts[:]:
                    made = self.utc.localize(datetime.utcfromtimestamp(x.created_utc)).astimezone(self.pacific)
                    if (made.strftime('%d%m%Y') == datetime.now(self.pacific).strftime('%d%m%Y')) and (
                            x.subreddit.display_name.lower() == self.subreddit):
                        team_lst = [self.teams[game['a']][1], self.teams[game['a']][2],
                                    self.teams[game['h']][1], self.teams[game['h']][2]]
                        check = sum(bool(y) for y in
                                    [team_lst[0].lower() in x.title.lower(), team_lst[1].lower() in x.title.lower(),
                                     team_lst[2].lower() in x.title.lower(), team_lst[3].lower() in x.title.lower(),
                                     'game thread' in x.title.lower(), 'gdt' in x.title.lower()])
                        pcheck = sum(bool(y) for y in ['post game thread' in x.title.lower(), 'pgt' in x.title.lower()])
                        if check >= 3 and pcheck == 0:
                            game_check[x] = check
                game_check_sorted = sorted(game_check.items(), key=lambda x: x[1], reverse=True)
                if len(game_check_sorted) > 0:
                    self.games[z]['thread'] = game_check_sorted[0][0]
                    self.games[z]['thread'].upvote()

    def update(self):
        final = [False] * len(self.games)

        self.find_gdt()

        w = requests.get(self.scheduleURL)
        data = json.loads(w.content.decode('utf-8'))['dates']
        w.close()

        if len(data) > 0:
            data=data[0]['games']

        for z in self.games:
            game = self.games[z]
            if game['time'] == 'Finished':
                final[z-1] = True
            else:
                for x in data[:]:
                    if x['gamePk'] == game['id']:
                        if x['linescore']['currentPeriod'] == 0:
                            time = 'Pre-game'
                        elif x['linescore']['currentPeriodTimeRemaining'] == 'Final':
                            time = 'Finished'
                        else:
                            time = x['linescore']['currentPeriodOrdinal'] + ' ' + \
                                   x['linescore']['currentPeriodTimeRemaining']
                        if time != self.games[z]['time']:
                            self.games[z]['time'] = time
                            print('{0} at {1} - {2}'.format(game['a'], game['h'], time))
                            if 'thread' in game.keys():
                                self.chatter_stats(x, game['thread'])

        if not self.games:
            print('No games today.')
            self.final = True
        elif all(final):
            self.final = True
            print('Games over for today.')
        else:
            sleep(60)

    def run(self):
        try:
            self.excluded = []
            self.date = datetime.now(self.pacific).strftime('%Y-%m-%d')
            self.scrape_games()
            while not self.final:
                self.update()
            while self.date == datetime.now(self.pacific).strftime('%Y-%m-%d'):
                sleep(300)
            self.run()
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(traceback.format_exc())

