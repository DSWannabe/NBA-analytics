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

def upsert_player_seasonal_stats(file_path):
    with db.atomic():
        for line in tqdm(
            open(file_path, encoding="utf-8"), mininterval=1, desc="seasonal"
        ):
            entry = json.loads(line)
            nba_seasonal_stats = {
                'player': entry['player'],
                'team': entry['team'],
                'year': entry['year'],
                'gp': entry['gp'],
                'wins': entry['wins'],
                'losses': entry['losses'],
                'mins': entry['min'],
                'pts': entry['pts'],
                'fgm': entry['fgm'],
                'fga': entry['fga'],
                'fgp': entry['fg_pct'],
                'three_pm': entry['three_pm'],
                'three_pa': entry['three_pa'],
                'three_ppct': entry['three_ppct'],
                'ftm': entry['ftm'],
                'fta': entry['fta'],
                'ft_pct': entry['ft_pct'],
                'oreb': entry['oreb'],
                'dreb': entry['dreb'],
                'reb': entry['reb'],
                'ast': entry['ast'],
                'tov': entry['tov'],
                'stl': entry['stl'],
                'blk': entry['blk'],
                'pf': entry['pf'],
                'fp': entry['fp'],
                'dd2': entry['dd2'],
                'td3': entry['td3'],
                'plus_minus_box': entry['plus_minus_box'],
            }
            NbaPlayerSeasonalStats.insert(nba_seasonal_stats).on_conflict(
                conflict_target=[
                    NbaPlayerSeasonalStats.team,
                    NbaPlayerSeasonalStats.player,
                    NbaPlayerSeasonalStats.year,
                    ],
                update=nba_seasonal_stats
            ).execute()

def upsert_player_game_stats(file_path):
    with db.atomic():
        for line in tqdm(
            open(file_path, encoding="utf-8"), mininterval=1, desc="game"
        ):
            entry = json.loads(line)
            nba_game_stats = {
                'player': entry['player'],
                'team': entry['team'],
                'against': entry['against'],
                'gamedate': datetime.strptime(entry['gamedate'], "%m/%d/%Y"),
                'min': entry['min'],
                'pts': entry['pts'],
                'fgm': entry['fgm'],
                'fga': entry['fga'],
                'fg_pct': entry['fg_pct'],
                'three_pm': entry['three_pm'],
                'three_pa': entry['three_pa'],
                'three_ppct': entry['three_ppct'],
                'ftm': entry['ftm'],
                'fta': entry['fta'],
                'ft_pct': entry['ft_pct'],
                'oreb': entry['oreb'],
                'dreb': entry['dreb'],
                'reb': entry['reb'],
                'ast': entry['ast'],
                'stl': entry['stl'],
                'blk': entry['blk'],
                'tov': entry['tov'],
                'pf': entry['pf'],
                'plus_minus_box': entry['plus_minus_box'],
                'fp': entry['fp'],
            }
            NbaPlayerGameStats.insert(nba_game_stats).on_conflict(
                conflict_target=[
                    NbaPlayerGameStats.player,
                    NbaPlayerGameStats.team,
                    NbaPlayerGameStats.against,
                    NbaPlayerGameStats.gamedate,
                ],
                update=nba_game_stats
            ).execute()

def upsert_team_info(file_path):
    with db.atomic():
        for line in tqdm(
            open(file_path, encoding="utf-8"), mininterval=1, desc="team"
        ):
            entry = json.loads(line)
            nba_team_info = {
                'team_name_full': entry['full_team_name'],
                'team': entry['team'],
            }
            NbaTeamInfo.insert(nba_team_info).on_conflict(
                conflict_target=[
                    NbaTeamInfo.team
                ],
                update=nba_team_info
            ).execute()

def upsert_player_info(file_path):
    with db.atomic():
        for line in tqdm(
            open(file_path, encoding="utf-8"), mininterval=1, desc="player"
        ):
            entry = json.loads(line)
            nba_player_info = {
                'player': entry['player'],
                'position': entry['position'],
                'height_ft': entry['height_ft'],
                'height_m': entry['height_m'],
                'weight_pounds': entry['weight_pounds'],
                'weight_kg': entry['weight_kg'],
                'birth': datetime.strptime(entry['birth'], "%Y-%m-%d"),
                'country': entry['country'],
                'draft_year': entry['draft_year'],
                'draft_round': entry['draft_round'],
                'draft_pick': entry['draft_pick'],
            }
            NbaPlayerInfo.insert(nba_player_info).on_conflict(
                conflict_target=[
                    NbaPlayerInfo.player_name,
                    NbaPlayerInfo.birth_date,
                ],
                update=nba_player_info
            ).execute()

if __name__ == "__main__":
    db.connect()
    upsert_player_seasonal_stats("data/nba_players_seasonal_stats.jsonl")
    # upsert_player_game_stats("data/nba_players_game_stats.jsonl")
    # upsert_team_info("data/teams_nba.jsonl")
    # upsert_player_info("data/player_info2.jsonl")
    db.close()