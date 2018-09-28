import json

def configure_get(category,name):
    with open ('tot.json','r') as f:
        conf = json.load(f)
        return conf[category][name]
