from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib as ur
import requests
import re
from csv import writer
import csv as csv
import ssl
import requests

# This restores the same behavior as before.
page = requests.get("https://www.aaii.com/sentimentsurvey?").text

soup = BeautifulSoup(page.content, 'html.parser')
bullClass = soup.find("div",{"class":"span-15"})
bullClassTwo = bullClass.find("div",{"class":"span-15"})

row = bullClassTwo.find_all('div') # Extract and return first occurrence of tr
dataString = str(soup)

print()

print(page)

print()

print(page.prettify()) # print the parsed data of html