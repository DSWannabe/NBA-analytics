import json
from datetime import datetime
from schema import (
    db,
    NbaPlayerSeasonalStats,
    NbaPlayerInfo,
    NbaTeamInfo,
    NbaPlayerGameStats
)
from tqdm import tqdm

def import_player_seasonal_stats(file_path):
    with db.atomic(), open(file_path, "r", encoding="utf-8") as file:

        for player in tqdm(file):
            player = json.loads(player)
            NbaPlayerSeasonalStats.create(
                player = player["player"],
                team = player["team"],
                year = player["year"],
                gp = player["gp"],
                wins = player["wins"],
                losses = player["losses"],
                mins = player["min"],
                pts = player["pts"],
                fgm = player["fgm"],
                fga = player["fga"],
                fgp = player["fg_pct"],
                three_pm = player["three_pm"],
                three_pa = player["three_pa"],
                three_ppct = player["three_ppct"],
                ftm = player["ftm"],
                fta = player["fta"],
                ft_pct = player["ft_pct"],
                oreb = player["oreb"],
                dreb = player["dreb"],
                reb = player["reb"],
                ast = player["ast"],
                tov = player["tov"],
                stl = player["stl"],
                blk = player["blk"],
                pf = player["pf"],
                fp = player["fp"],
                dd2 = player["dd2"],
                td3 = player["td3"],
                plus_minus_box = player["plus_minus_box"]
            )

def import_nba_team_info(file_path):
    with db.atomic(), open(file_path, "r", encoding="utf-8") as file:
        for team in tqdm(file):
            team = json.loads(team)
            NbaTeamInfo.create(
                team_name_full = team["full_team_name"],
                team_name_short = team["team"],
            )

def import_nba_player_game_stats(file_path):
    with db.atomic(), open(file_path, "r", encoding="utf-8") as file:
        for player in tqdm(file):
            player = json.loads(player)
            NbaPlayerGameStats.create(
                player_name = player["player"],
                team = player["team"],
                against = player["against"],
                gamedate = player["gamedate"],
                w_l = player["w_l"],
                min = player["min"],
                pts = player["pts"],
                fgm = player["fgm"],
                fga = player["fga"],
                fg_pct = player["fg_pct"],
                three_pm = player["three_pm"],
                three_pa = player["three_pa"],
                three_ppct = player["three_ppct"],
                ftm = player["ftm"],
                fta = player["fta"],
                ft_pct = player["ft_pct"],
                oreb = player["oreb"],
                dreb = player["dreb"],
                reb = player["reb"],
                ast = player["ast"],
                stl = player["stl"],
                blk = player["blk"],
                tov = player["tov"],
                pf = player["pf"],
                plus_minus_box = player["plus_minus_box"],
                fp = player["fp"]
            )

def import_nba_player_info(file_path):
    with db.atomic(), open(file_path, "r", encoding="utf-8") as file:
        for player in tqdm(file):
            player = json.loads(player)
            NbaPlayerInfo.create(
                player_name = player["player"],
                birth= player["birth"],
                country = player["country"],
                height_feet = player["height_ft"],
                height_m = player["height_m"],
                weight_pounds = player["weight_pounds"],
                weight_kg = player["weight_kg"],
                draft_year = player["draft_year"],
                draft_round = player["draft_round"],
                draft_pick = player["draft_pick"],
            )

if __name__ == "__main__":
    db.connect()
    db.create_tables(
        [
            NbaPlayerSeasonalStats,
            NbaPlayerInfo,
            NbaTeamInfo,
            NbaPlayerGameStats
        ]
    )
    import_player_seasonal_stats("data/nba_players_seasonal_stats.jsonl")
    import_nba_player_game_stats("data/nba_players_game_stats.jsonl")
    import_nba_team_info("data/teams_nba.jsonl")
    import_nba_player_info("data/players_info2.jsonl")

    db.close()