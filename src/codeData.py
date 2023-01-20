from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

website = requests.get("https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html")

webpageResponse = website.content

soup = BeautifulSoup(webpageResponse, "html.parser")

data = soup.find_all(attrs={"class": "Rating"})


ratings = []

for system in data[1:]:
  ratings.append(float(system.get_text()))
print(ratings)

plt.hist(ratings)
plt.show()



#print(soup.td.string)

