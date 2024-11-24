from fastapi import FastAPI, Query, HTTPException
from database.schema import (
    db,
    NbaPlayerSeasonalStats,
    NbaPlayerInfo
)
from typing import Optional, List
import polars as pl
from peewee import fn

app = FastAPI(
    title="NBA Stats API",
    description="An API to query NBA stats"
)

@app.on_event("startup")
async def startup():
    if db.is_closed():
        db.connect()

@app.on_event("shutdown")
async def shutdown():
    if not db.is_closed():
        db.close()

@app.get("/search/")
async def search_player(name: str):
    try:
        player = NbaPlayerSeasonalStats.select().where(
            NbaPlayerSeasonalStats.player.contains(name)
        ).dicts()

        result = list(player)
        if not result:
            raise HTTPException(status_code=404, detail="Player not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/quartile/")
async def quartile_stats(
    name: str = Query(None, description="Player name"),
    year: str = Query(None, description="Year of the season (e.g:, '2024')")
):
    try:
        # player's stats
        player = list(NbaPlayerSeasonalStats.select().where(
            (NbaPlayerSeasonalStats.player.contains(name)) &
            (NbaPlayerSeasonalStats.year == year)
        ).dicts())

        # league's stats
        league = list(NbaPlayerSeasonalStats.select().where(
            NbaPlayerSeasonalStats.year == year
        ).dicts())

        player_df = pl.DataFrame(player)
        league_df = pl.DataFrame(league)

        # check if player exists
        if player_df.is_empty():
            raise HTTPException(status_code=404, detail="Player not found")

        # check if league exists
        if league_df.is_empty():
            raise HTTPException(status_code=404, detail="Year not found")

        # calculate quartiles
        stats = ['pts', 'ast', 'reb', 'stl', 'blk', 'plus_minus_box']
        result = {}

        for stat in stats:
            quartiles = league_df.select(
                [
                    pl.col(stat).quantile(0.25).alias("Q1"),
                    pl.col(stat).quantile(0.5).alias("Q2"),
                    pl.col(stat).quantile(0.75).alias("Q3"),
                    pl.col(stat).quantile(0.95).alias("Q4")
                ]
            )

            player_stat = float(player_df[stat][0])

            result[stat] = {
                f"{stat}": player_stat,
                "league quartiles": {
                    "Q1": float(quartiles['Q1'][0]),
                    "Q2": float(quartiles['Q2'][0]),
                    "Q3": float(quartiles['Q3'][0]),
                    "Q4": float(quartiles['Q4'][0])
                },
                "percentile": round(float(
                    (league_df[stat] < player_stat).sum() / len(league_df[stat]) * 100), 2)
            }

        # Calculate efficiency metrics with proper float conversion
        efficiency_metrics = {
            "true_shooting": round(
                float(player_df['pts'][0]) / 
                (2 * (float(player_df['fga'][0]) + 0.44 * float(player_df['fta'][0])))
                * 100, 2
            ),
            "assist_ratio": round(
                float(player_df['ast'][0]) / float(player_df['mins'][0]) * 100, 
                2
            ),
            "turnover_ratio": round(
                float(player_df['tov'][0]) / float(player_df['mins'][0]) * 100, 
                2
            ),
            "usage_rate": round(
                (float(player_df['fga'][0]) + 0.44 * float(player_df['fta'][0]) + 
                float(player_df['tov'][0])) / float(player_df['mins'][0]) * 100, 
                2
            )
        }

        # Calculate league averages
        league_efficiency = {
            "true_shooting": round(
                league_df['pts'].mean() / 
                (2 * (league_df['fga'].mean() + 0.44 * league_df['fta'].mean()))
                * 100, 2
            ),
            "assist_ratio": round(
                league_df['ast'].mean() / league_df['mins'].mean() * 100,
                2
            ),
            "turnover_ratio": round(
                league_df['tov'].mean() / league_df['mins'].mean() * 100,
                2
            ),
            "usage_rate": round(
                (league_df['fga'].mean() + 0.44 * league_df['fta'].mean() + 
                league_df['tov'].mean()) / league_df['mins'].mean() * 100,
                2
            )
        }
        """
        TS% = PTS / (2 * (FGA + 0.44 * FTA)) * 100 : Takes into account all shots
        AST% = AST / MIN * 100
        TOV% = TOV / MIN * 100
        USG% = (FGA + 0.44 * FTA + TOV) / MIN * 100 : How often a player attempts to make shots/turnovers/free throuws in a game

        0.44 is the average number of free throws per field goal attempt in the NBA. It's a widely 
        used constant in basketball analytics to estimate the number of free throw attempts based on
        the number of field goal attempts.
        """

        # Format efficiency metrics with comparisons
        efficiency_comparison = {
            metric: {
                "player_value": player_value,
                "league_average": league_efficiency[metric],
                "difference": round(player_value - league_efficiency[metric], 2)
            }
            for metric, player_value in efficiency_metrics.items()
        }

        return {
            "Player": name,
            'Year': year,
            'Statistics': result,
            'Efficiency Metrics': efficiency_comparison
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the NBA Stats API"}

