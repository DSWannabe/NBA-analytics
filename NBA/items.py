# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

@dataclass
class nba_scraping:
    PlayerIDYear: str
    player: str
    team_playerseason: str
    year_playerseason: int
    age_playerseason: int
    gp_playerseason: int
    wins_playerseason: int
    losses_playerseason: int
    min_playerseason: float
    pts_playerseason: float
    fgm_playerseason: float
    fga_playerseason: float
    fg_pct_playerseason: float
    three_pm_playerseason: float
    three_pa_playerseason: float
    three_ppct_playerseason: float
    ftm_playerseason: float
    fta_playerseason: float
    ft_pct_playerseason: float
    oreb_playerseason: float
    dreb_playerseason: float
    reb_playerseason: float
    ast_playerseason: float
    tov_playerseason: float
    stl_playerseason: float
    blk_playerseason: float
    pf_playerseason: float
    fp_playerseason: float
    dd2_playerseason: float
    td3_playerseason: float
    plus_minus_box_playerseason: float
    

@dataclass
class player_game_stats:
    player: str
    team_playergame: str
    against_playergame: str
    gamedate_playergame: str
    w_l_playergame: str
    min_playergame: float
    pts_playergame: float
    fgm_playergame: int
    fga_playergame: int
    fg_pct_playergame: float
    three_pm_playergame: int
    three_pa_playergame: int
    three_ppct_playergame: float
    ftm_playergame: int
    fta_playergame: int
    ft_pct_playergame: float
    oreb_playergame: int
    dreb_playergame: int
    reb_playergame: int
    ast_playergame: int
    stl_playergame: int
    blk_playergame: int
    tov_playergame: int
    pf_playergame: int
    plus_minus_box_playergame: int
    fp_playergame: float

@dataclass
class player_urls_lst:
    player_url: str

@dataclass
class player_info:
    player: str
    height_ft: str
    height_m: str
    weight_pounds: str
    weight_kg: str
    country: str
    birth: str
    draft_year: str
    draft_round: str
    draft_pick: str
    player_id: str

@dataclass
class game_results:
    team_team: str
    matchup_team: str
    gamedate_team: str
    w_l_team: str
    min_team: str
    pts_team: str
    fgm_team: str
    fga_team: str
    fg_pct_team: str
    three_pm_team: str
    three_pa_team: str
    three_pct_team: str
    ftm_team: str
    fta_team: str
    ft_pct_team: str
    oreb_team: str
    dreb_team: str
    reb_team: str
    ast_team: str
    stl_team: str
    blk_team: str
    tov_team: str
    pf_team: str
    plus_minus_box_team: str