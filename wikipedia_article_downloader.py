import requests

text = ""
r = requests.get("https://www.wikizeroo.org/index.php?q=aHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvVmljaWFfZmFiYQ")
if r.status_code == 200:
    text = r.text
else:
    text = "no text"
print(text)