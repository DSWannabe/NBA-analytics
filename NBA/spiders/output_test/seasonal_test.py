import json
from collections import defaultdict

# Initialize a defaultdict to store the count of players for each year
yearly_player_count = defaultdict(int)

# Open the JSONL file
with open('/home/anhtupham99/NBA-analytics/data/nba_players_seasonal_stats.jsonl', 'r', encoding='utf-8') as file:
    for line in file:
        # Parse the JSON object from the line
        data = json.loads(line.strip())

        # Extract the year (assuming the key is 'year')
        year = data.get('year')
        # Increment the count for the year
        if year:
            yearly_player_count[year] += 1

# Print the results
for year, count in yearly_player_count.items():
    print(f"Year: {year}, Players: {count}")