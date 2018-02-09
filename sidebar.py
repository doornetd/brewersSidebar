#!/usr/bin/env python2.7

from __future__ import print_function
from bs4 import BeautifulSoup
from urllib2 import urlopen
import requests
import praw
from datetime import datetime

MY_SUB = "brewerstest"
MY_USERNAME = 'BrewersBort'
MY_PASSWORD = 'CubsSuck69'
MY_USER_AGENT = 'Sidebar updater by /u/BrewersBort'
MY_CLIENT_ID = 'iZZZ8xUDjPT5eQ'
MY_CLIENT_SECRET = 'Xe4PEOPswOZ5nKcFkqjWfFvBuEo'

WILDCARD_URL = 'https://nytimes.stats.com/mlb/standings_wildcard.asp'
FANGRAPHS_URL = 'http://www.fangraphs.com/teams/brewers'
TRANS_URL = 'http://www.spotrac.com/mlb/transactions/milwaukee-brewers/'

player_codes = {'Jesus Aguilar': '[](/aguilar)',
                'Chase Anderson': '[](/anderson)',
                'Orlando Arcia': '[](/arcia)',
                'Jett Bandy': '[](/bandy)',
                'Jacob Barnes': '[](/barnes)',
                'Ryan Braun': '[](/braun)',
                'Keon Broxton': '[](/broxton)',
                'Lorenzo Cain': '[](/cain)',
                'Zach Davies': '[](/davies)',
                'Junior Guerra': '[](/guerra)',
                'Josh Hader': '[](/hader)',
                'Jeremy Jeffress': '[](/jeffress)',
                'Corey Knebel': '[](/knebel)',
                'Jimmy Nelson': '[](/nelson)',
                'Hernan Perez': '[](/perez)',
                'Brett Phillips': '[](/phillips)',
                'Manny Pina': '[](/pina)',
                'Domingo Santana': '[](/santana)',
                'Travis Shaw': '[](/shaw)',
                'Eric Sogard': '[](/sogard)',
                'Brent Suter': '[](/suter)',
                'Eric Thames': '[](/thames)',
                'Jonathan Villar': '[](/villar)',
                'Stephen Vogt': '[](/vogt)',
                'Aaron Wilkerson': '[](/wilkerson)',
                'Christian Yelich': '[](/yelich)',
                'Jhoulys Chacin': '[](/chacin)',
                'Yovani Gallardo': '[](/gallardo)',
                'Adrian Houser': '[](/houser)',
                'Boone Logan': '[](/logan)',
                'Jorge Lopez': '[](/lopez)',
                'Freddy Peralta': '[](/peralta)',
                'Jacob Nottingham': '[](/nottingham)',
                'Andrew Susac': '[](/susac)',
                'Tyler Webb': '[](/webb)',
                'Mauricio Dubon': '[](/dubon)',
                'Marcos Diplan': '[](/diplan)'}

pitcher_urls = [['http://www.fangraphs.com/statsd.aspx?playerid=sa828677&position=P', 'Ortiz', '[](/prospect-ortiz)'],
                ['http://www.fangraphs.com/statsd.aspx?playerid=sa873673&position=P', 'Burnes', '[](/prospect-burnes)'],
                ['http://www.fangraphs.com/statsd.aspx?playerid=sa737343&position=P', 'Peralta', '[](/prospect-peralta)'],
                ['http://www.fangraphs.com/statsd.aspx?playerid=sa828590&position=P', 'Diplan', '[](/prospect-diplan)'],
                ['http://www.fangraphs.com/statsd.aspx?playerid=sa828707&position=P', 'Supak', '[](/prospect-supak)']]

position_urls = [['http://www.fangraphs.com/statsd.aspx?playerid=sa738510&position=OF', 'Ray', '[](/prospect-ray)'],
                 ['http://www.fangraphs.com/statsd.aspx?playerid=sa3004043&position=2B', 'Hiura', '[](/prospect-hiura)'],
                 ['http://www.fangraphs.com/statsd.aspx?playerid=sa3004968&position=OF', 'Lutz', '[](/prospect-lutz)'],
                 ['http://www.fangraphs.com/statsd.aspx?playerid=sa738378&position=2B/SS', 'Dubon', '[](/prospect-dubon)'],
                 ['http://www.fangraphs.com/statsd.aspx?playerid=sa872722&position=3B', 'Erceg', '[](/prospect-erceg)']]

positionl_urls = [[('http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat'
                  '&lg=all&qual=100&type=8&season=2017&month=0&season1=2017'
                  '&ind=0&team=23&rost=0&age=0&filter=&players=0&sort=20,d'), 20, 'WAR'],
                [('http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat'
                  '&lg=all&qual=100&type=8&season=2017&month=0&season1=2017'
                  '&ind=0&team=23&rost=0&age=0&filter=&players=0&sort=16,d'), 16, 'wRC+'],
                [('http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat'
                  '&lg=all&qual=100&type=8&season=2017&month=0&season1=2017'
                  '&ind=0&team=23&rost=0&age=0&filter=&players=0&sort=4,d'), 4, 'HR'],
                [('http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat'
                  '&lg=all&qual=100&type=8&season=2017&month=0&season1=2017'
                  '&ind=0&team=23&rost=0&age=0&filter=&players=0&sort=12,d'), 12, 'AVG']]
pitchingl_urls = [[('https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit'
                    '&lg=all&qual=20&type=8&season=2017&month=0&season1=2017'
                    '&ind=0&team=23&rost=0&age=0&filter=&players=0&sort=18,d'), 18, 'WAR'],
                [('https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit'
                    '&lg=all&qual=20&type=8&season=2017&month=0&season1=2017'
                    '&ind=0&team=23&rost=0&age=0&filter=&players=0&sort=15,a'), 15, 'ERA'],
                [('https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit'
                    '&lg=all&qual=20&type=8&season=2017&month=0&season1=2017'
                    '&ind=0&team=23&rost=0&age=0&filter=&players=0&sort=16,a'), 16, 'FIP'],
                [('https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit'
                    '&lg=all&qual=20&type=8&season=2017&month=0&season1=2017'
                    '&ind=0&team=23&rost=0&age=0&filter=&players=0&sort=8,d'), 8, 'K/9']]

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
    
    #find injury table from fangraphs
    soup = setupSoup(FANGRAPHS_URL)

    injury_table = []
    brewer_injuries = soup.find_all('table')[8].find_all('tr')
    injury_table.append(["Player", "Injury", "Status"])
    for row in brewer_injuries:
        temp_array = []
        cells = row.find_all('td')
        for cell in cells:
            temp_array.append(cell.string)
        if('No Recent Injuries' in temp_array[0]):
            temp_array = ["No", "Recent", "Injuries"]
        else:
            if temp_array[0] in player_codes:
                temp_array[0] = player_codes[temp_array[0]]
        injury_table.append(temp_array)
    injuries = parseTable(injury_table, "## Injury Report")

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
    '''
    #find transactions table from fangraphs
    trans_table = []
    brewer_trans = soup.find_all('table')[10].find_all('tr')
    trans_table.append(["Date", "Transaction"])
    count = 0
    for row in brewer_trans:
        if(count < 5):
            temp_array = []
            cells = row.find_all('td')
            for cell in cells:
                temp_array.append(cell.string)
            trans_table.append(temp_array)
            count += 1
    transactions = parseTable(trans_table, "## Recent Transactions")
    '''
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

    position_leaders = parseTable(positionl_table, "## Batting Leaders")
    pitching_leaders = parseTable(pitchingl_table, "## Pitching Leaders")    
    
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

