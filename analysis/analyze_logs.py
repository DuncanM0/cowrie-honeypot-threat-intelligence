import json

with open('cowrie.json') as f:
    d = json.load(f)
    print(d)
