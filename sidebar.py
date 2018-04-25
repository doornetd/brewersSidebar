#!/usr/bin/env python2.7

from __future__ import print_function
from bs4 import BeautifulSoup
from urllib2 import urlopen
import requests
import re
import praw
from player_codes import player_codes
from stat_urls import pitcher_urls, position_urls, positionl_urls, pitchingl_urls
from datetime import datetime

MY_SUB = "brewers"
MY_USERNAME = 'BrewersBort'
MY_PASSWORD = 'CubsSuck69'
MY_USER_AGENT = 'Sidebar updater by /u/BrewersBort'
MY_CLIENT_ID = 'iZZZ8xUDjPT5eQ'
MY_CLIENT_SECRET = 'Xe4PEOPswOZ5nKcFkqjWfFvBuEo'

WILDCARD_URL = 'https://nytimes.stats.com/mlb/standings_wildcard.asp'
FANGRAPHS_URL = 'https://www.fangraphs.com/teams/brewers'
SPOTRAC_URL = 'http://www.spotrac.com/mlb/milwaukee-brewers/payroll/'
TRANS_URL = 'http://www.spotrac.com/mlb/transactions/milwaukee-brewers/'


#---------------------------------------------------------------------    

def parseTable(stats_table, header):

    #print(header + '\n')
    returner = ''
    returner += header + '\n\n'
    
    #print batter stats
    sep_string = ''
    for y in range(0, len(stats_table)):
        for x in range(0, len(stats_table[y])):
            returner += stats_table[y][x]
            if x < len(stats_table[y])-1:
                returner += ' | '
                sep_string+=':-:|'
            else:
                sep_string+=':-:'
                returner += '\n'
        if y == 0:
            returner += sep_string + '\n'
    returner += '\n\n'

    return returner

#---------------------------------------------------------------------

def setup_reddit():
    
    reddit = praw.Reddit(client_id=MY_CLIENT_ID,
        client_secret=MY_CLIENT_SECRET,
        password=MY_PASSWORD,
        user_agent=MY_USER_AGENT,
        username=MY_USERNAME)

    print("Authenticated as {}".format(reddit.user.me()))

    return reddit

#---------------------------------------------------------------------

def setupSoup(the_url):
    html = urlopen(the_url).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

#---------------------------------------------------------------------    

def main():
    #setup reddit
    reddit = setup_reddit()

    #find wildcard table from NYT
    soup = setupSoup(WILDCARD_URL)
    '''
    nl_table = soup.find_all('table')[2].find_all('tr')

    wildcard_table = []
    for i in range(1,8):
        row = nl_table[i]
        cells = row.find_all(['th', 'td'])
        team = ''
        if i == 1:
            wildcard_table.append([cells[0].string, cells[1].string, cells[2].string, cells[3].string, cells[4].string])
        elif i != 4:
            team = cells[0].find('a').string
            wildcard_table.append([team, cells[1].string, cells[2].string, cells[3].string, cells[4].string])
    wildcard = parseTable(wildcard_table, '## Wildcard Standings')
    '''
    #-------------------------------
    
    #---------Fangraphs injuries--------
    #Find injury table from fangraphs
    soup = setupSoup(FANGRAPHS_URL)
    injury_table = []
    injury_table.append(["Player", "Injury", "Status"])
    brewer_injuries = soup.find_all('table')[8].find_all('tr')
    for row in brewer_injuries:
       temp_array = []
       cells = row.find_all('td')
       temp_array = [cells[0].string, cells[1].string, cells[2].string]
       if temp_array[0] in player_codes:
          temp_array[0] = player_codes[temp_array[0]]
       injury_table.append(temp_array)
    injuries = parseTable(injury_table, "## Injury Report")
       

    '''
    #---------Spotrac injuries---------- 	
    #find injury table from spotrac
    soup = setupSoup(SPOTRAC_URL)

    injury_table = []
    brewer_injuries = soup.find_all('table')[1].find_all('tr')
    injury_table.append(["Player", "Status"])
    for row in range(1, len(brewer_injuries)):
        temp_array = []
        cell = brewer_injuries[row].find('td')
	name = cell.find('a').string
	status = cell.find_all('span')[1].string
	status = re.sub('[()]', '', status)
	temp_array.append(name)
	temp_array.append(status)
        if temp_array[0] in player_codes:
                temp_array[0] = player_codes[temp_array[0]]
        injury_table.append(temp_array)
    injuries = parseTable(injury_table, "## Injury Report")
    '''

    #-------------------------------

    #find transactions table from spotrac
    soup = setupSoup(TRANS_URL)
    trans_table = []
    trans_table.append(["Player", "Transaction"])
    count = 0

    brewer_trans = soup.find_all('article')
    for row in brewer_trans:
        if(count < 5):
            date = row.find_all('span')[1].text
            name = row.find('a').text
            detail = row.find('p').text
            trans_table.append([name, detail])
            #print(date + " " + name + " " + detail)
            count += 1
    transactions = parseTable(trans_table, "## Recent Transactions")   
    
    #-------------------------------

    #find pitching and batting prospect last game statistics
    pitching_table = []
    position_table = []
    pitching_table.append(["Player", "Lvl", "IP", "ER", "H", "BB"])
    position_table.append(["Player", "Lvl", "AB", "H", "BB", "HR"])

    for url in pitcher_urls:
        soup = setupSoup(url[0])
        temp_array = []
        
        body = soup.find_all('tbody')[3]
        row = body.find_all('tr')[2]
        cells = row.find_all('td')

        level = cells[1].string[5:-1]
        tag = "[](" + url[0] + ") " + url[1]
        now = datetime.strptime(cells[0].string, '%Y-%m-%d').date()
        gamedate = now.strftime('%B %d, %Y')
        pitching_table.append([gamedate, '', '', '', '', ''])
        pitching_table.append([tag, level, cells[10].string, cells[14].string, cells[12].string, cells[16].string])

        '''
        adv_url = url[0] + '&type=-2&gds=&gde=&season=2017'
        soup = setupSoup(adv_url)
        temp_array = []

        body = soup.find_all('tbody')[3]
        row = body.find_all('tr')[0]
        cells = row.find_all('td')
        pitching_table.append(['Season', 'ERA', 'FIP', 'WHIP', 'K/9', 'BB/9'])
        pitching_table.append(['', cells[15].string, cells[16].string, cells[12].string, cells[4].string, cells[5].string])
        '''
        #print(tag + " " + level + " " + cells[10].string + " " + cells[14].string + " " + cells[12].string + " " + cells[16].string)
        
    for url in position_urls:        
        soup = setupSoup(url[0])
        temp_array = []
        
        body = soup.find_all('tbody')[3]
        row = body.find_all('tr')[2]
        cells = row.find_all('td')

        level = cells[1].string[5:-1]
        tag = "[](" + url[0] + ") " + url[1]
        now = datetime.strptime(cells[0].string, '%Y-%m-%d').date()
        gamedate = now.strftime('%B %d, %Y')
        position_table.append([gamedate, '', '', '', '', ''])
        position_table.append([tag, level, cells[4].string, cells[6].string, cells[13].string, cells[10].string])

        '''
        adv_url = url[0] + '&type=-2&gds=&gde=&season=2017'
        soup = setupSoup(adv_url)
        temp_array = []

        body = soup.find_all('tbody')[3]
        row = body.find_all('tr')[0]
        cells = row.find_all('td')
        
        position_table.append(['Season', 'AVG', 'OBP', 'SLG', 'K%', 'wRC+'])
        position_table.append(['', cells[6].string, cells[7].string, cells[8].string, cells[4].string, cells[17].string])
        #print(tag + " " + level + " " + cells[4].string + " " + cells[6].string + " " + cells[13].string + " " + cells[10].string)
        '''
            
    pitching = parseTable(pitching_table, "## Pitching Prospects Update")
    position = parseTable(position_table, "## Position Prospects Update")
    
    #-------------------------------  
    #find pitching and batting leaaders
    pitchingl_table = []
    positionl_table = []
    pitchingl_table.append(["Cat.", "Player", "Total"])
    positionl_table.append(["Cat.", "Player", "Total"])

    for url in positionl_urls:
        soup = setupSoup(url[0])

        temp_array = []
        
        body = soup.find_all('tbody')[1]
        row = body.find_all('tr')
        for i in range(0,3):
            temp_row = row[i]
            cells = temp_row.find_all('td')
            if i == 0:
                name = cells[1].string
                if name in player_codes:
                    name = player_codes[name] + name
                positionl_table.append([url[2], name, cells[url[1]].string])
                #print(url[2] + ' ' + cells[1].string + ' ' + cells[url[1]].string)
            else:
                positionl_table.append(['', cells[1].string, cells[url[1]].string])
                #print('    ' + ' ' + cells[1].string + ' ' + cells[url[1]].string)
    
    for url in pitchingl_urls:
        soup = setupSoup(url[0])

        temp_array = []
        
        body = soup.find_all('tbody')[1]
        row = body.find_all('tr')
        for i in range(0,3):
            temp_row = row[i]
            cells = temp_row.find_all('td')
            if i == 0:
                name = cells[1].string
                if name in player_codes:
                    name = player_codes[name] + name
                pitchingl_table.append([url[2], name, cells[url[1]].string])
                #print(url[2] + ' ' + cells[1].string + ' ' + cells[url[1]].string)
            else:
                pitchingl_table.append(['', cells[1].string, cells[url[1]].string])
                #print('    ' + ' ' + cells[1].string + ' ' + cells[url[1]].string)

    position_leaders = parseTable(positionl_table, "## Batting Leaders \n# *qualififed batters")
    pitching_leaders = parseTable(pitchingl_table, "## Pitching Leaders \n# *min. 10 IP")    
    
    #-------------------------------  
    #grab the text from the sidebar and split
    subreddit = reddit.subreddit(MY_SUB)
    sidebar = subreddit.description
    new_text = sidebar.split("[](/brewersbort)")

    #parse wildcard table into string and combine final sidebar string
    final_text = new_text[0] + "[](/brewersbort)\n\n" \
        + injuries + transactions \
        + pitching + position \
        + position_leaders + pitching_leaders \
        + '[](/brewersbort)' + new_text[2]

    #print(final_text)

    #update sidebar with new text
    subreddit.mod.update(description=final_text)
    print("Updated " + MY_SUB + " at " +  str(datetime.now()))
#---------------------------------------------------------------------    

if __name__ == "__main__":
    main() 

