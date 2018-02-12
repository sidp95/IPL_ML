import csv
import os
import numpy as np
import argparse
import sys
import math
import utilscsv
from collections import OrderedDict
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String , or_, and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sqlite3
from sklearn.neural_network import MLPClassifier 
from sklearn.preprocessing import normalize, scale

if __name__ == '__main__':
	argv = sys.argv[1:]

	parser = argparse.ArgumentParser()
	parser.add_argument('-q','--question', required=True, choices=['1', '2', '3', '4', '5' , '6', '7', '8'])

	io_args = parser.parse_args()
	question = io_args.question


	if question == '1':

		files = os.listdir("/Users/Sid/Documents/ResearchPAPER-NEURALIPL/Data/2014")
		if files[0] == '.DS_Store':
			files.remove('.DS_Store')
		path = "/Users/Sid/Documents/ResearchPAPER-NEURALIPL/Data/2014/"
		count = 0
		for file in files:
			path_now = path + file
			print(file)
			data = utilscsv.CSV_parser(path_now)
			namesz = utilscsv.retrieve_names(data)
			team1 = namesz[0]
			team2 = namesz[1] 
			winner = utilscsv.winner(data)

			won_by = utilscsv.won_by(data)

			season = utilscsv.season(data)

			date = utilscsv.date(data)
			# Dict of innings of each team
			innings_one, innings_two = utilscsv.innings(data,team1)
			# Getting names of players from each team, to see how much they scored or otherwise

			team_name1, team_name2 = utilscsv.player_names(innings_one, innings_two)
			
			dict_team1_runs = utilscsv.num_runs_scored(team_name1, innings_one)

			dict_team2_runs = utilscsv.num_runs_scored(team_name2, innings_two)

			# wickets taken, innings and team name of batsmen here is swapped since the bowling
			# team are the ones taking wickets from their opposite innings taem
			dict_wickets_team1 = utilscsv.wickets_taken(team_name1, innings_two)
			dict_wickets_team2 = utilscsv.wickets_taken(team_name2, innings_one)
			# print(dict_wickets_team1)

			# SO far we have the following information: 		

			## Just doing team1 

			# Team1 score
			overs_faced_team1 ,runs_scored_team1 = utilscsv.team_score(dict_team1_runs)

			# team1 wickets taken 
			wickets_taken_by_team1 = utilscsv.sum_wickets_taken(dict_wickets_team1)
			# print("number of wickets taken by team : ", wickets_taken_by_team1)
			
			## DOING team2

			# Team2 score
			overs_faced_team2 , runs_scored_team2 = utilscsv.team_score(dict_team2_runs)
			wickets_taken_by_team2 = utilscsv.sum_wickets_taken(dict_wickets_team2)

			print("Team1 name: ", team1, "Team2 Name: ", team2, "runs scored: ",runs_scored_team1, "runs scored: ", runs_scored_team2, "overs faced team1: ", overs_faced_team1, "team2: ", overs_faced_team2, "team1 w :", wickets_taken_by_team1, "team2 w: ", wickets_taken_by_team2,"winner is : ", winner)
			
			print()

	if question == '2':
		print("Starting Database testing...")

		# FIX THE FOLLOWING!


		print("Initialzing engine..")
		engine = create_engine('sqlite:///:testdata:', echo=False)
		Base = declarative_base()

		class Team(Base):
			__tablename__ = 'teams'
			id = Column(Integer, primary_key = True)
			team1 = Column(String)
			team2 = Column(String)
			runs_team1 = Column(Integer)
			runs_team2 = Column(Integer)
			overs_team1 = Column(Integer)
			overs_team2 = Column(Integer)
			wickets_team1 = Column(Integer)
			wickets_team2 = Column(Integer)
			winner_game = Column(String)
			date_game = Column(Integer)

		# class User(Base):
		# 	__tablename__ = 'users'
		# 	id = Column(Integer, primary_key = True)
		# 	name = Column(String)
		# 	fullname = Column(String)
		# 	password = Column(String)

		Base.metadata.create_all(engine)


		print("Class created")

		print("creating session!")


		Session = sessionmaker(bind=engine)
		session = Session()
		# session.add(User(name = "yomamam"))
		# session.add(Team(team1 = "Kolkata"))

		session.add(Team(team1 = "Kolkata Knight Rider", team2 = "Royal Challengers Bangalore" , runs_team1 = 222, runs_team2 = 82, overs_team1 = 20, overs_team2 = 16, wickets_team1 = 10, wickets_team2 = 3, date_game = 20080419, winner_game = "Kolkata Knight Riders"))
		session.commit()




		print("closing session")


		session.close()





		print("successful yaya!")
	if question == '3':

		print("Starting Database testing...")


		print("Initialzing engine..")
		engine = create_engine('sqlite:///:ipl2008:', echo=False)
		Base = declarative_base()
		# class User(Base):
		# 	__tablename__ = 'users'
		# 	id = Column(Integer, primary_key = True)
		# 	name = Column(String)
		# 	fullname = Column(String)
		# 	password = Column(String)

		class Team(Base):
			__tablename__ = 'teams'
			id = Column(Integer, primary_key = True)
			team1 = Column(String)
			team2 = Column(String)
			runs_team1 = Column(Integer)
			runs_team2 = Column(Integer)
			overs_team1 = Column(Integer)
			overs_team2 = Column(Integer)
			wickets_team1 = Column(Integer)
			wickets_team2 = Column(Integer)
			winner_game = Column(Integer)
			date_game = Column(Integer)

		print("Class created")

		print("creating session!")


		Session = sessionmaker(bind=engine)
		session = Session()

		# WRITE QUERIES HERE


		# retrieve the list of dates as an arary and store it
		lst = []
		for instance in session.query(Team):
			lst.append(instance.date_game)

		# for each date in list, retrieve the previous matches:

		date = lst[3]

		# The following code retrives the games before the date in question

		for instance in session.query(Team).filter(Team.date_game < date):
			print("teams played are: ", instance.team1)

			

		print("closing session")
		session.close()

	if question == '4':
		# # Combining storing things in the database and the code for extraction:
		print("works yaya")
		# print("Starting Database testing...")

		# # FIX THE FOLLOWING!


		# print("Initialzing engine..")
		# engine = create_engine('sqlite:///:ipl2008:', echo=False)
		# Base = declarative_base()

		# class Team(Base):
		# 	__tablename__ = 'teams'
		# 	id = Column(Integer, primary_key = True)
		# 	team1 = Column(String)
		# 	team2 = Column(String)
		# 	runs_team1 = Column(Integer)
		# 	runs_team2 = Column(Integer)
		# 	overs_team1 = Column(Integer)
		# 	overs_team2 = Column(Integer)
		# 	wickets_team1 = Column(Integer)
		# 	wickets_team2 = Column(Integer)
		# 	winner_game = Column(String)
		# 	date_game = Column(Integer)

		# # class User(Base):
		# # 	__tablename__ = 'users'
		# # 	id = Column(Integer, primary_key = True)
		# # 	name = Column(String)
		# # 	fullname = Column(String)
		# # 	password = Column(String)

		# Base.metadata.create_all(engine)


		# print("Class created")

		# print("creating session!")


		# Session = sessionmaker(bind=engine)
		# session = Session()
		# # session.add(User(name = "yomamam"))
		# # session.add(Team(team1 = "Kolkata"))

		# ## Code from part 1!

		# files = os.listdir("/Users/Sid/Documents/ResearchPAPER-NEURALIPL/Data/Ipl_test_csv")
		# files.remove('.DS_Store')
		# path = "/Users/Sid/Documents/ResearchPAPER-NEURALIPL/Data/Ipl_test_csv/"
		# count = 0
		# for file in files:
		# 	path_now = path + file
		# 	# print(path_now)
		# 	data = utilscsv.CSV_parser(path_now)
		# 	namesz = utilscsv.retrieve_names(data)
		# 	team1 = namesz[0]
		# 	team2 = namesz[1] 
		# 	winner = utilscsv.winner(data)

		# 	won_by = utilscsv.won_by(data)

		# 	season = utilscsv.season(data)

		# 	date = utilscsv.date(data)
		# 	# Dict of innings of each team
		# 	innings_one, innings_two = utilscsv.innings(data,team1)
		# 	#print(innings_two[1])
		# 	# Getting names of players from each team, to see how much they scored or otherwise

		# 	team_name1, team_name2 = utilscsv.player_names(innings_one, innings_two)
			
		# 	dict_team1_runs = utilscsv.num_runs_scored(team_name1, innings_one)
		# 	# print(dict_team1_runs)

		# 	dict_team2_runs = utilscsv.num_runs_scored(team_name2, innings_two)
			
		# 	# print(dict_team2_runs)
		# 	# wickets taken, innings and team name of batsmen here is swapped since the bowling
		# 	# team are the ones taking wickets from their opposite innings taem
		# 	dict_wickets_team1 = utilscsv.wickets_taken(team_name1, innings_two)
		# 	dict_wickets_team2 = utilscsv.wickets_taken(team_name2, innings_one)
		# 	# print(dict_wickets_team1)

		# 	# SO far we have the following information: 		

		# 	## Just doing team1 

		# 	# Team1 score
		# 	overs_faced_team1 ,runs_scored_team1 = utilscsv.team_score(dict_team1_runs)
		# 	# print(runs_scored_team1)
		# 	# print(overs_faced_team1)

		# 	# team1 wickets taken 
		# 	wickets_taken_by_team1 = utilscsv.sum_wickets_taken(dict_wickets_team1)
		# 	# print("number of wickets taken by team : ", wickets_taken_by_team1)
			
		# 	## DOING team2

		# 	# Team2 score
		# 	overs_faced_team2 , runs_scored_team2 = utilscsv.team_score(dict_team2_runs)
		# 	wickets_taken_by_team2 = utilscsv.sum_wickets_taken(dict_wickets_team2)
		# 	# print(runs_scored_team2)
		# 	# print(overs_faced_team2)

		# 	# print("Name of team1 is : ", team2)
		# 	# print("They faced ", overs_faced_team2, "overs and scored ", runs_scored_team2, "and lost ", wickets_taken_by_team1, "wickets")
		# 	# print("And took a  total of ", wickets_taken_by_team2, "wickets when they were bowling")
		# 	# print()
		# 	# print("Their batting dict is : ", dict_team2_runs)
		# 	# print()
		# 	# print("Their bowling dict is : ", dict_wickets_team2)
		# 	# print()
		# 	# print("won by Team: ", winner)
		# 	# print( "date time is : ", date)

		# 	# print("Team1 name: ", team1, "Team2 Name: ", team2, "runs scored: ",runs_scored_team1, "runs scored: ", runs_scored_team2, "overs faced team1: ", overs_faced_team1, "team2: ", overs_faced_team2, "team1 w :", wickets_taken_by_team1, "team2 w: ", wickets_taken_by_team2,"winner is : ", winner)
		# 	print(winner)
		# 	session.add(Team(team1 = team1, team2 = team2 , runs_team1 = runs_scored_team1 , runs_team2 = runs_scored_team2, overs_team1 = overs_faced_team1 , overs_team2 = overs_faced_team2, wickets_team1 = wickets_taken_by_team1, wickets_team2 = wickets_taken_by_team2, date_game = date, winner_game = winner))

		# ### Use the session.add method to add in each loop!

		# # session.add(Team(team1 = "Kolkata Knight Rider", team2 = "Royal Challengers Bangalore" , runs_team1 = 222, runs_team2 = 82, overs_team1 = 20, overs_team2 = 16, wickets_team1 = 10, wickets_team2 = 3, date_game = 20080419))
		
		# #Commit at the very end

		# session.commit()

		# print("closing session")

		# session.close()

		# print("everything done")
	if question == '5' :
		# Databases: 'ipl2008.db', ipl2010, ipl2011, ipl2012, ipl2013, ipl2014, ipl2015, ipl2016
		# Instead of using different database connections, will save them as different tables in same databse!
		#DAta base = ipl 
		conn = sqlite3.connect('ipl.db')
		c = conn.cursor()

		# tables names: ipl2008  (ipl + year)

		c.execute('''CREATE TABLE ipl2016
		(id Integer PRIMARY KEY, team1 text, team2 text, runs_team1 Integer, runs_team2 Integer, overs_team1 Integer, overs_team2 Integer,wickets_team1 Integer, wickets_team2 Integer, winner_game Integer, date_game Integer)''')


		files = os.listdir("/Users/Sid/Documents/ResearchPAPER-NEURALIPL/Data/2016")
		if files[0] == '.DS_Store':
			files.remove('.DS_Store')
		path = "/Users/Sid/Documents/ResearchPAPER-NEURALIPL/Data/2016/"
		count = 0
		for file in files:
			path_now = path + file
			# print(path_now)
			data = utilscsv.CSV_parser(path_now)
			namesz = utilscsv.retrieve_names(data)
			team1 = namesz[0]
			team2 = namesz[1] 
			winner = utilscsv.winner(data)

			won_by = utilscsv.won_by(data)

			season = utilscsv.season(data)

			date = utilscsv.date(data)
			# Dict of innings of each team
			innings_one, innings_two = utilscsv.innings(data,team1)
			#print(innings_two[1])
			# Getting names of players from each team, to see how much they scored or otherwise

			team_name1, team_name2 = utilscsv.player_names(innings_one, innings_two)
			
			dict_team1_runs = utilscsv.num_runs_scored(team_name1, innings_one)
			# print(dict_team1_runs)

			dict_team2_runs = utilscsv.num_runs_scored(team_name2, innings_two)
			
			# print(dict_team2_runs)
			# wickets taken, innings and team name of batsmen here is swapped since the bowling
			# team are the ones taking wickets from their opposite innings taem
			dict_wickets_team1 = utilscsv.wickets_taken(team_name1, innings_two)
			dict_wickets_team2 = utilscsv.wickets_taken(team_name2, innings_one)
			# print(dict_wickets_team1)

			# SO far we have the following information: 		

			## Just doing team1 

			# Team1 score
			overs_faced_team1 ,runs_scored_team1 = utilscsv.team_score(dict_team1_runs)
			# print(runs_scored_team1)
			# print(overs_faced_team1)

			# team1 wickets taken 
			wickets_taken_by_team1 = utilscsv.sum_wickets_taken(dict_wickets_team1)
			# print("number of wickets taken by team : ", wickets_taken_by_team1)
			
			## DOING team2

			# Team2 score
			overs_faced_team2 , runs_scored_team2 = utilscsv.team_score(dict_team2_runs)
			wickets_taken_by_team2 = utilscsv.sum_wickets_taken(dict_wickets_team2)
			t = (count, team1, team2, runs_scored_team1, runs_scored_team2, overs_faced_team1, overs_faced_team2, wickets_taken_by_team1, wickets_taken_by_team2, winner, date )
			count = count + 1


			c.execute("INSERT INTO ipl2016 VALUES ( ?, ?,  ? ,  ?,  ?,  ?, ?, ?,  ?,  ?, ?)", t)
		print("successful")

		conn.commit()

		# # We can also close the connection if we are done with it.
		# Just be sure any changes have been committed or they will be lost.
		conn.close()

		print("connection closed")
	if question == '6':

		# Queries and statistics calculation

		conn = sqlite3.connect('ipltest.db')
		c = conn.cursor()

		# t = ('Kolkata Knight Rider',)
		# c.execute('SELECT team1 FROM teams')
		# wrd = c.fetchall()
		# print(wrd)

		# Basic variables:
		teamz1 = "Kolkata Knight Riders"
		teamz2 = "Mumbai Indians"
		# teamz1 = teamz2
		ids = 15

		# WIN percentage ========================================================================================================================================
		win_percentage = 0

		games_played = 0
		games_won = 0

		# for row in c.execute('SELECT COUNT(*) FROM teams WHERE date_game < 20080429 AND (team1 = "Kolkata Knight Riders" OR team2 = "Kolkata Knight Riders" )'):
		# 	print(row[0])
		p = (teamz1,teamz1)

		c.execute('SELECT COUNT(*) FROM teams WHERE date_game < 20080429 AND (team1 = ? OR team2 = ? )', p)
		games_played = c.fetchone()[0]

		q = (teamz1,teamz1, teamz1)
		
		c.execute('SELECT COUNT(*) FROM teams WHERE date_game < 20080429 AND (team1 = ? OR team2 = ? ) AND winner_game = ?', q)
		games_won = c.fetchone()[0]
		print(games_won)

		win_percentage = games_won / games_played
		print("win percentage", win_percentage)

		# ========================================================================================================================================

		# Batting Run rate:

		batting_run_rate = 0
		sum_runs_scored_team1 = 0
		team1_overs_faced = 0

		t = (teamz1,)
		c.execute('SELECT SUM(runs_team1) FROM teams WHERE date_game < 20080429 AND team1 = ?', t)
		sum_runs_scored_team1 = c.fetchone()[0]
		c.execute('SELECT SUM(runs_team2) FROM teams WHERE date_game < 20080429 AND team2 = ?', t)
		sum_runs_scored_team1 = sum_runs_scored_team1 + c.fetchone()[0]
		# print(sum_runs_scored_team1)

		t = (teamz1,)

		c.execute('SELECT SUM(overs_team1) FROM teams WHERE date_game < 20080429 AND team1 = ?', t)
		team1_overs_faced = c.fetchone()[0]
		c.execute('SELECT SUM(overs_team2) FROM teams WHERE date_game < 20080429 AND team2 = ?', t)
		team1_overs_faced = team1_overs_faced + c.fetchone()[0]
		# print(team1_overs_faced)

		batting_run_rate = sum_runs_scored_team1/team1_overs_faced
		print("batting run rate", batting_run_rate)

		# ====================================================================================================================================
		# BOWLING ECONOMY RATE

		bowling_economy = 0
		runs_conceded = 0
		overs_bowled = 0

		t = (teamz1,)
		c.execute('SELECT SUM(runs_team2) FROM teams WHERE date_game < 20080429 AND team1 = ?', t)
		runs_conceded = c.fetchone()[0]

		c.execute('SELECT SUM(runs_team1) FROM teams WHERE date_game < 20080429 AND team2 = ?', t)
		runs_conceded = runs_conceded + c.fetchone()[0]


		c.execute('SELECT SUM(overs_team2) FROM teams WHERE date_game < 20080429 AND team1 = ? ', t)
		overs_bowled = c.fetchone()[0]
		c.execute('SELECT SUM(overs_team1) FROM teams WHERE date_game < 20080429 AND team2 = ? ', t)
		overs_bowled = overs_bowled + c.fetchone()[0]





		bowling_economy = runs_conceded / overs_bowled
		print("bowling economy", bowling_economy)
		# ====================================================================================================================================
		
		# Batting AVG

		batting_average = 0
		team2_wickets = 0

		t = (teamz1,)
		c.execute('SELECT SUM(wickets_team2) FROM teams WHERE date_game < 20080429 AND team1 = ?', t)
		team2_wickets = c.fetchone()[0]
		print(team2_wickets)

		
		c.execute('SELECT SUM(wickets_team1) FROM teams WHERE date_game < 20080429 AND team2 = ?', t)

		team2_wickets = team2_wickets + c.fetchone()[0]
		batting_average = sum_runs_scored_team1 / team2_wickets



		print("team batting average" ,batting_average)
		# ====================================================================================================================================
		
		# Bowling average
		bowling_average = 0
		wickets_taken = 0

		t = (teamz1,)
		c.execute('SELECT SUM(wickets_team1) FROM teams WHERE date_game < 20080429 AND team1 = ?', t)
		wickets_taken = c.fetchone()[0]
		

		
		c.execute('SELECT SUM(wickets_team2) FROM teams WHERE date_game < 20080429 AND team2 = ?', t)

		wickets_taken = wickets_taken + c.fetchone()[0]

		bowling_average = runs_conceded / wickets_taken
		print("bowing average ", bowling_average)

		# ====================================================================================================================================

		# BAtting wicket rate:

		batting_wicket_rate =   (team1_overs_faced* 6) /team2_wickets 
		print("batting wicket rate", batting_wicket_rate)

		# Bowling strike rate:
		bowling_strike_rate = (overs_bowled* 6) / wickets_taken 
		print("bowling strike rate", bowling_strike_rate)

		# Batting Index:
		Batting_index = batting_run_rate * batting_average

		Bowling_index = bowling_economy * bowling_average

		print("batting index: ", Batting_index)
		
		print("bowling index: ", Bowling_index)

		for row in c.execute('SELECT team1,team2,date_game FROM teams ORDER BY date_game ASC'):
			print(row)




		conn.close()
		print("closing")

	if question == '7':
		# ipltest

		######
		# Choosing number of features in the feature set
		num_features = 4
		num_features_combined = num_features*2

		# conn = sqlite3.connect('ipltest.db')
		conn = sqlite3.connect('ipl.db')
		c = conn.cursor()
		names = ['ipl2008','ipl2010','ipl2011','ipl2012','ipl2013','ipl2015','ipl2016']
		dictionary = {}

		for folder in names:
			files = os.listdir("/Users/Sid/Documents/Research_Projects/ResearchPAPER-NEURALIPL/Data/" + folder)
			if files[0] == '.DS_Store':
				files.remove('.DS_Store')
			# files.remove('.DS_Store')
			path = "/Users/Sid/Documents/ResearchPAPER-NEURALIPL/Data/" + folder
			count = 0
			for file in files:
				count = count + 1
				# print(file)

			dictionary[folder]= count
		print(dictionary)
		# CREATE matrices related to each table name

		# 2008 matrix base

		matrix_2008 = np.zeros((dictionary['ipl2008'],num_features))
		Y_2008 = np.zeros(dictionary['ipl2008'])
		matrix_2010 = np.zeros((dictionary['ipl2010'],num_features))
		Y_2010 = np.zeros(dictionary['ipl2010'])
		matrix_2011 = np.zeros((dictionary['ipl2011'],num_features))
		Y_2011 = np.zeros(dictionary['ipl2011'])
		matrix_2012 = np.zeros((dictionary['ipl2012'],num_features))
		Y_2012 = np.zeros(dictionary['ipl2012'])
		matrix_2013 = np.zeros((dictionary['ipl2013'],num_features))
		Y_2013 = np.zeros(dictionary['ipl2013'])
		matrix_2015 = np.zeros((dictionary['ipl2015'],num_features))
		Y_2015 = np.zeros(dictionary['ipl2015'])
		matrix_2016 = np.zeros((dictionary['ipl2016'],num_features))
		Y_2016 = np.zeros(dictionary['ipl2016'])
		


		# Table name // CHANGE HERE TO GET THINGS WORKING
		# tablename = "teams"
		tablenames = ['ipl2008','ipl2010','ipl2011','ipl2012','ipl2013','ipl2015','ipl2016']

		for tablename in tablenames:


			dates = []
			team1s = []
			team2s = []
			winner = []
			numcols = dictionary[tablename]

			for row in c.execute('SELECT team1, team2, date_game, winner_game FROM '+tablename+' ORDER BY date_game ASC'):
				team1s.append(row[0])
				team2s.append(row[1])
				dates.append(row[2])
				winner.append(row[3])


			# print(dates[0])
			# print(team1s[0])
			# print(team2s[0])
			part1 = utilscsv.matrix_creator(c,tablename,team1s[0], dates[0])
			part2 = utilscsv.matrix_creator(c,tablename,team2s[0], dates[0])
			matrix = np.concatenate((part1, part2))
			# print("MATRIX SHAPE ", matrix.shape)
			# ('Kolkata Knight Riders', 'Mumbai Indians', 20080429)
			




			for i in range(1,numcols):
				ans1 = utilscsv.matrix_creator(c, tablename,team1s[i], dates[i])
				ans2 = utilscsv.matrix_creator(c, tablename,team2s[i], dates[i])
				ans = np.concatenate((ans1,ans2))
				matrix = np.concatenate((matrix, ans))
				# print("DONE")

			matrix.shape = (numcols,num_features_combined)
			win_array = utilscsv.win_array(team1s, winner)
			# a = utilscsv.matrix_creator(c,tablename,'Kolkata Knight Riders', 20080429)
			# b = utilscsv.matrix_creator(c,tablename,'Mumbai Indians', 20080429)
			# c = np.concatenate((a,b))
			# # print("manuall : ",c )

			if tablename == 'ipl2008':
				matrix_2008 = matrix
				Y_2008 = win_array
			elif tablename == 'ipl2010':
				matrix_2010 = matrix 
				Y_2010 = win_array
			elif tablename == 'ipl2011':
				matrix_2011 = matrix 
				Y_2011 = win_array
			elif tablename == 'ipl2012':
				matrix_2012 = matrix 
				Y_2012 = win_array
			elif tablename == 'ipl2013':
				matrix_2013 = matrix 
				Y_2013 = win_array
			elif tablename == 'ipl2015':
				matrix_2015 = matrix 
				Y_2015 = win_array
			elif tablename == 'ipl2016':
				matrix_2016 = matrix 
				Y_2016 = win_array
		print("done")

		# print(matrix_2013[40], "result",Y_2013[40])
			









			# DEAL WITH CREATING WIN_ARRAY LATER!!
			# print("IS MY PROGRAM CORRECT? ", matrix[15]== c)
			# win_array = utilscsv.win_array(team1s, winner)
		# print(toprint)

		# conn.close()
		print("closing")
		conn.close()





		# Combine most of the matrices and their corresponding result vectors:
		X = np.concatenate((matrix_2008, matrix_2010))
		X = np.concatenate((X,matrix_2011))
		X = np.concatenate((X,matrix_2012))
		X = np.concatenate((X,matrix_2013))
		X = np.concatenate((X,matrix_2015))
		X = np.concatenate((X,matrix_2016))
		# X = np.concatenate((X,matrix_2016))

		# Combine correspoinding Y lists
		Y = np.concatenate((Y_2008, Y_2010))
		Y = np.concatenate((Y, Y_2011))
		Y = np.concatenate((Y, Y_2012))
		Y = np.concatenate((Y, Y_2013))
		Y = np.concatenate((Y, Y_2015))
		Y = np.concatenate((Y, Y_2016))

		# Y = np.concatenate((Y, Y_2016))
		# validation set is ipl2016!
		# Y_valid = np.concatenate((Y_2015, Y_2016))
		# print(len(Y_valid))


		
		



		# print(matrix.shape)
		# print(win_array.shape)

		# PreProcessing the Data

		# Normalize the columns

		X = scale(X)
		print(X.shape)
		# X_valid_2011 = scale(matrix_2011)
		X_valid_2012 = scale(matrix_2012)
		# print(X_valid_2011[7])


		# X_valid = np.concatenate((matrix_2015, matrix_2016))
		# X_valid = normalize(X_valid)
		# print("shape of you ", X_valid.shape)
		# print(X[15])
		# print(Y_2016)
		# print(len(Y_2016))

		# # # MACHINE LEARNING PART (FINALLY)
		# smallest = np.inf
		# highest = 0

		# for i in range(20):
		# print(X)
		# iterval = 0
		# for i in range(10):
			



		# fit
		model = MLPClassifier(solver = 'lbfgs', hidden_layer_sizes = 40, activation = 'relu')
			# print("training...")

		model.fit(X,Y)

		Y_predict = model.predict(X)
		denom = len(Y)
		tr_error = sum(Y_predict == Y)/denom
		print("Accuracy is ", tr_error)

			# # print("Predicting..")
			# Y_predict = model.predict(X_valid_2011)

			# denom = len(Y_2011)
				

			# error = sum(Y_predict != Y_2011)/denom
			# print("error for 2011 dataset is : ", error)

		# Y_predict = model.predict(X_valid_2012)

		# denom = len(Y_2012)
		# error = sum(Y_predict != Y_2012)/denom
		# print("error for 2015 dataset is : ", error)




		# print("correct percentage is is(first try so super shitty) :", error*100)
		# 	# print(Y_predict)
		# if error < smallest:
		# 	smallest = error
		# elif error > highest:
		# 	highest = error
		# print("highest error:  ", highest)
		# print("lowest error: ", smallest)
		# print("...terminated...")

		# model = MLPClassifier(solver = 'lbfgs', hidden_layer_sizes = 100, activation = 'relu')
		# # print("training...")

		# model.fit(X,Y)

		# # print("Predicting..")
		# Y_predict = model.predict(X_valid_2016)

		# denom = len(Y_2016)
			

		# error = sum(Y_predict == Y_2016)/denom
		# print("error for 2016 dataset is : ", error)











	if question == '8':

		names = ['ipl2008','ipl2010','ipl2011','ipl2012','ipl2013','ipl2015','ipl2016']
		dictionary = {}
		total_count = 0

		for folder in names:
			files = os.listdir("/Users/Sid/Documents/Research_Projects/ResearchPAPER-NEURALIPL/Data/" + folder)
			if files[0] == '.DS_Store':
				files.remove('.DS_Store')
			# files.remove('.DS_Store')
			path = "/Users/Sid/Documents/Research_Projects/ResearchPAPER-NEURALIPL/Data/" + folder
			count = 0
			for file in files:
				count = count + 1
				# print(file)
			total_count = total_count + count
			

			dictionary[folder]= count
		print(dictionary['ipl2008'])
		print("totalcount ", total_count)









		

		





		
		




		
