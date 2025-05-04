import re

pattern = r"/player/(\d+)/career/"
lst = []

with open("/home/node/files/data/player_urls.jsonl") as file:
    for line in file.read().splitlines():
        match = re.search(pattern, line)
        if match:
            player_id = match.group(1)
            lst.append(player_id)
print(lst)