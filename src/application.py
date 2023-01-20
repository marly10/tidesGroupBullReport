from flask import Flask
import requests
from bs4 import BeautifulSoup
import re


# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'

instructions2 = '''
    <p><em>The Bull Report</em> </p>\n'''

footer_text = '</body>\n</html>'

page = requests.get("https://www.aaii.com/sentimentsurvey?")
soup = BeautifulSoup(page.content, 'html.parser')
bullClass = soup.find("div",{"class":"span-15"})
bullClassTwo = bullClass.find("div",{"class":"span-15"})

row = bullClassTwo.find_all('div') # Extract and return first occurrence of tr
dataString = str(row)

url = requests.get(f"https://finance.yahoo.com/quote/%5EVIX/")
sp = BeautifulSoup(url.content, 'html.parser')
vixData = sp.find(id="quote-header-info")
vix = vixData.find_all(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
data = str(vixData)

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
say_hello() + instructions + instructions2 + footer_text + data + str(row)))

# add a rule when the page is accessed with a name appended to the site
# URL.Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)data
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
