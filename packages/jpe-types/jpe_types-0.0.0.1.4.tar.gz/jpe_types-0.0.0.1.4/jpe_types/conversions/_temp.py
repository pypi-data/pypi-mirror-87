import json

data = {}

data["baseKeys"] = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_+"


with open("intConversions.json", "w") as wfile:
    json.dump(data, wfile)