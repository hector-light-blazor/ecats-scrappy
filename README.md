
# ecats-scrappy
The name of the program is Ecats Scrappy.

# Operating System

The operating system I used to build the program is Windows.
May work on linux or mac os havent tried.

# Dependancies & Python Version

Python Version 3.8

1.) Selenium

2.) psycopg2

3.) win32api

IF need a binary use the following
pyinstaller
This allows without distrubtion of having python install in other windows environment.

# Publish Project
10-22-2020

# Author Contact
My name is Hector Chapa.

You can reach me at roensebastian2015@gmail.com for any 
questions of this project.

# PURPOSE:
Get information from a particular website and autonamous runs report. Scrapes the information from the website submits to PostGreSQL.

# File BreakDowns
1.) main.py: Where everything starts.

2.) SQLMod.py: contains the functions regarding SQL interactions to the database.

3.) WebMod.py: contains the functions regarding browser interactions using selenium.

4.) SysMod.py: contains the functions regarding interacting with the operating system regarding getting all available drives.

5.) config.init: File contains configurations for the program to consume. If the file is updated the program will adapt.
For example, if I add more custom reports from the website, once added in the config.init the program will scrape the information without pausing and re-execution.
