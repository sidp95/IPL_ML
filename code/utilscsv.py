import os
import numpy as np
import csv
from collections import OrderedDict
import numpy as np

def CSV_parser(path):
	# get each row of the csv file and put it into a dict indexed from 1
	match_dict = OrderedDict()
	with open(path, 'r') as f:
		reader = csv.reader(f, delimiter=';')
		counter = 1
		for row in reader:
			match_dict[counter] = row 
			counter = counter + 1
	return match_dict


def retrieve_names(match):
	team1 = match[2][0].split(',')[2]
	team2 = match[3][0].split(',')[2]
	namesz = [team1,team2]
	first_team = match[21][0].split(',')[3]
	if namesz[0] == first_team:
		team1 = first_team
		team2 = namesz[1]
	elif namesz[1] == first_team:
		team1 = namesz[1]
		team2 = namesz[0]
	return [team1, team2]


def winner(dict_match):
	rt_val = ""
	for i in range(1, 21):
		if dict_match[i][0].split(',')[1] == "winner":
			rt_val = dict_match[i][0].split(',')[2]


	return rt_val

def won_by(dict_match):
	return dict_match[20][0].split(',')[2]

def season(dict_match):
	return dict_match[5][0].split(',')[2]

def date(dict_match): 
	string = dict_match[6][0].split(',')[2]
	string = string.replace('/', '')
	return int(string)




# Takes input of the dictionary and the name of team1 (return value of retrieve_name_1()) 

def innings(dict_match, team1):
	# row 21 is from where 
	innings_one = OrderedDict()
	innings_two = OrderedDict()
	counter1 = 1
	counter2 = 1

	for i in range(21,len(dict_match)+1):
		if dict_match[i][0].split(',')[3] == team1:
			innings_one[counter1] = dict_match[i][0].split(',')
			counter1 = counter1 + 1
		else:
			innings_two[counter2] = dict_match[i][0].split(',')
			counter2 = counter2 + 1

	return innings_one, innings_two



def player_names(team1, team2):
	names_team1 = []
	names_team2 = []
	for i in range(1, len(team1)+1):
		player_team1 = team1[i][4]
		player_team2 = team1[i][6]

		if player_team1 not in names_team1:
			names_team1.append(player_team1)

		if player_team2 not in names_team2:
			names_team2.append(player_team2)

	for i in range(1, len(team2)+1):
		player_team2 = team2[i][4]
		player_team1 = team2[i][6]

		if player_team2 not in names_team2:
			names_team2.append(player_team2)

		if player_team1 not in names_team1:
			names_team1.append(player_team1)
			
	return names_team1, names_team2

#improved version above
# def player_name(team1, team2):
# 	names_team1 = []
# 	for i in range(1,len(team1)+1):
# 		names_team1.append(team1[i][0].split(',')[4])

# 	for i in range(1, len(team2)+1):
# 		names_team1.append(team2[i][0].split(',')[6])

# 	teamnamez = []
# 	for name in names_team1:
# 		if name not in teamnamez:
# 			teamnamez.append(name)
			

# 	return teamnamez

#  =============== ===============
# a = {}
# 		key = "somekey"
# 		a.setdefault(key,[])
# 		a[key].append(1)
# 		print(a[key])


#  =============== ===============


# MIGHT REMOVE EXTRAS AS PART OF GAME


# Takes list of names of players and their innings
# Returns a dict of player names + their strike rate
def num_runs_scored(player_names, team_innings):
	
	#dic = dict.fromkeys(player_names, 0)
	dic = {name : [0,0,0] for name in player_names}
	dic["extras"] = 0

	for key, value in team_innings.items():
		dic[value[4]][0] = dic[value[4]][0] + int(value[7])
		dic[value[4]][1] = dic[value[4]][1] + 1
		dic["extras"] = dic["extras"] + int(value[8])

	
	return dic

# Takes a list of names of players and their innings
# Returns a dict of player names as key, with the wickets and runs consumed
# as associated values

def wickets_taken(player_names,team_innings):
	dic = {name : [0,0,0] for name in player_names}
	dic["run_outs"] = 0

	for key, value in team_innings.items():
		dic[value[6]][0] = dic[value[6]][0] + int(value[7]) + int(value[8])
		dic[value[6]][1] = dic[value[6]][1] + 1
		result = value[9]
		if result == "caught" or result== "bowled" or result == "lbw":
			dic[value[6]][2] = dic[value[6]][2] + 1
		# if value[9] == "bowled":
			# dic[value[6]][2] = dic[value[6]][2] + 1
		if value[9] == "run out":
			dic["run_outs"] = dic["run_outs"] + 1
		


	return dic 

def first_team(match, team1):
	return match[21][0].split(',')[3]


def team_score(Dict):
	runs_scored = 0
	overs_bowled = 0
	for Key, Value in Dict.items():
		if type(Value) == int:
			runs_scored = runs_scored + Value
		else :
			runs_scored = runs_scored + Value[0]
			overs_bowled = overs_bowled + Value[1]
	overs_bowled = overs_bowled/6
	return overs_bowled, runs_scored

# Takes a Dict of a team's wicket taking dict (from wickets_taken() ), returns the 
# number of wickets captured by that particular team

def sum_wickets_taken(Dict):
	wickets_taken = 0
	for Key, Value in Dict.items():
		# print("Value", Value)
		
		if type(Value) == int:
			wickets_taken = wickets_taken + Value
		else :
			wickets_taken= wickets_taken + Value[2]
		# print(wickets_taken)
	return wickets_taken

# Test function
def cursorobj(c):
	c.execute('SELECT COUNT(date_game) FROM teams')
	numrows = c.fetchone()[0]
	print(numrows)

def error_handle(item):
	if item == None:
		item = 0
	return item


# Signature: Sqlite Cursor Object,teamname, date  -> numpy array  
# Takes a curson object from a database
# Outputs a 9 element numpy array
# stored in database and 9 is number of types of statistical calculations

def matrix_creator(c, tablename,teamname, dategame):

	# val to return initialization
	ans = np.zeros(4)

	# Win percentage
	win_percentage = 0
	games_played = 0
	games_won = 0
	p = (dategame, teamname, teamname)
	c.execute('SELECT COUNT(*) FROM '+tablename+' WHERE date_game < ? AND (team1 = ? OR team2 = ? )', p)
	games_played = c.fetchone()[0]
	p = (dategame, teamname,teamname, teamname)
	c.execute('SELECT COUNT(*) FROM '+tablename+' WHERE date_game < ? AND (team1 = ? OR team2 = ? ) AND winner_game = ?', p)
	games_won = c.fetchone()[0]
	if games_played != 0:
		win_percentage = games_won/games_played
	# print("win percentage: ", win_percentage)
	ans[0]= win_percentage





	# Batting Run rate:
	batting_run_rate = 0
	sum_runs_scored = 0
	total_overs_faced = 0

	p = (dategame, teamname)
	c.execute('SELECT SUM(runs_team1) FROM '+tablename+' WHERE date_game < ? AND team1 = ?', p)
	sum_runs_scored = c.fetchone()[0]
	sum_runs_scored =  error_handle(sum_runs_scored)
	c.execute('SELECT SUM(runs_team1) FROM '+tablename+' WHERE date_game < ? AND team2 = ?', p)
	temp = c.fetchone()[0]
	temp = error_handle(temp)
	sum_runs_scored = sum_runs_scored +  temp
	# print(sum_runs_scored)

	p = (dategame,teamname)
	c.execute('SELECT SUM(overs_team1) FROM '+tablename+' WHERE date_game < ? AND team1 = ?', p)
	total_overs_faced = error_handle(c.fetchone()[0])

	c.execute('SELECT SUM(overs_team2) FROM '+tablename+' WHERE date_game < ? AND team2 = ?', p)
	total_overs_faced = total_overs_faced + error_handle(c.fetchone()[0])

	if total_overs_faced != 0:
		batting_run_rate = sum_runs_scored/total_overs_faced
	# print("batting run rate : ", batting_run_rate)
	# ans[1]= batting_run_rate






	# Bowling ECONOMY RATE:
	bowling_economy = 0
	runs_conceded = 0
	overs_bowled = 0

	p = (dategame, teamname)
	c.execute('SELECT SUM(runs_team2) FROM '+tablename+' WHERE date_game < ? AND team1 = ?', p)
	runs_conceded = error_handle(c.fetchone()[0])
	c.execute('SELECT SUM(runs_team1) FROM '+tablename+' WHERE date_game < ? AND team2 = ?', p)
	runs_conceded = runs_conceded + error_handle(c.fetchone()[0])

	c.execute('SELECT SUM(overs_team2) FROM '+tablename+' WHERE date_game < ? AND team1 = ? ', p)
	overs_bowled = error_handle( c.fetchone()[0])
	c.execute('SELECT SUM(overs_team1) FROM '+tablename+' WHERE date_game < ? AND team2 = ? ', p)
	overs_bowled = overs_bowled + error_handle( c.fetchone()[0])

	if overs_bowled != 0:
		bowling_economy = runs_conceded/overs_bowled
	# print("bowling economy rate: ", bowling_economy)
	# ans[2]= bowling_economy






	# Batting AVG
	batting_average = 0
	team2_wickets = 0
	p = (dategame, teamname)
	c.execute('SELECT SUM(wickets_team2) FROM '+tablename+' WHERE date_game < ? AND team1 = ?', p)
	team2_wickets = error_handle(c.fetchone()[0])
	c.execute('SELECT SUM(wickets_team1) FROM '+tablename+' WHERE date_game < ? AND team2 = ?', p)
	team2_wickets = team2_wickets + error_handle(c.fetchone()[0])
	if team2_wickets != 0:
		batting_average = sum_runs_scored / team2_wickets
	# print("Batting averaeg: ", batting_average)
	# ans[3]= batting_average


	


	# Bowling AVG
	bowling_average = 0
	wickets_taken = 0
	p = (dategame,teamname)
	c.execute('SELECT SUM(wickets_team1) FROM '+tablename+' WHERE date_game < ? AND team1 = ?', p)
	wickets_taken = error_handle(c.fetchone()[0])
	c.execute('SELECT SUM(wickets_team2) FROM '+tablename+' WHERE date_game < ? AND team2 = ?', p)
	wickets_taken = wickets_taken + error_handle(c.fetchone()[0])

	if wickets_taken != 0:
		bowling_average = runs_conceded/wickets_taken
	# print("Bowling average: ", bowling_average)
	# ans[4]= bowling_average




	# Batting Wicket Rate
	batting_wicket_rate = 0
	if team2_wickets != 0:
		batting_wicket_rate = (total_overs_faced * 6)/team2_wickets
	# print("batting_wicket_rate : ", batting_wicket_rate)
	# ans[5]= batting_wicket_rate



	# Bowling strike rate
	bowling_strike_rate = 0
	if wickets_taken != 0:
		bowling_strike_rate = (overs_bowled * 6) / wickets_taken
	# print("bowling strike rate: ", bowling_strike_rate)
	# ans[6]= bowling_strike_rate



	# Batting Index
	Batting_index = batting_run_rate * batting_average

	# print("Batting_index ", Batting_index)
	# ans[7]= Batting_index

	# Bowling Index
	Bowling_index = bowling_economy * bowling_average
	# print("Bowling_index",Bowling_index)
	# ans[8]= Bowling_index
	ans[1]= batting_run_rate - bowling_economy
	ans[2] = batting_average - bowling_average
	ans[3] = batting_wicket_rate - bowling_strike_rate




	return ans 

def win_array(firstteam, winner):
	length = len(winner)
	toreturn = np.ones(length)
	for i in range(length):
		if firstteam[i] == winner[i]:
			toreturn[i] = 0
	return toreturn















	




	







				    				


	
	




 












	


