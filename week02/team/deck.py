import requests

response = requests.get('https://deckofcardsapi.com/api/deck/ehwqfhqgnhop/draw')
#print(response.json())

json = response.json()

cards = json["cards"]

print(cards)