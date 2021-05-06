import json

with open("datasets/p2/tv_shows_to_index_final.json") as f:
  data = json.load(f)
f.close()

print(list(map((lambda x: x.lower()), list(data.keys()))))