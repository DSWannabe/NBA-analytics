# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

@dataclass
class nba_scraping:
    player: str
    team: str
    age: int
    gp: int
    wins: int
    losses: int
    min : float
    pts: float
    fgm: float
    fga: float
    fg_pct: float
    three_pm: float
    three_pa: float
    three_ppct: float
    ftm: float
    fta: float
    ft_pct: float
    oreb: float
    dreb: float
    reb: float
    ast: float
    tov: float
    stl: float
    blk: float
    pf: float
    fp: float
    dd2: float
    td3: float
    plus_minus_box: float

@dataclass
class game_stats:
    player: str
    team: str
    matchup: str
    gamedate: str
    w_l: str
    min: float
    pts: float
    fgm: int
    fga: int
    fg_pct: float
    three_pm: int
    three_pa: int
    three_ppct: float
    ftm: int
    fta: int
    ft_pct: float
    oreb: int
    dreb: int
    reb: int
    ast: int
    stl: int
    blk: int
    tov: int
    pf: int
    plus_minus_box: int
    fp: float

@dataclass
class player_urls_lst:
    player_url: str

@dataclass
class player_info:
    player: str
    height_feet: str
    height_cm: str
    weight_pounds: str
    weight_kg: str
    country: str
    draft: str
    birth: str