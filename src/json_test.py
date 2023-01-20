import urllib, json, requests, pprint

def json_return():
    url = "https://api.punkapi.com/v2/beers"
    url_reponse = requests.get(url)
    print(url_reponse.ok)

    data = json.loads(url_reponse.text)

    count = 0
    for i in range(len(data)):
        #if data[i]["name"] == username: #username = name, pass = target_og
         #   count+=1
          #  print("found: "+str(count))
          
     return {
                "username": data[i]["name"],
                "extra": data[i]["tagline"],
                "password": data[i]["target_og"],
            }


print(json_return())