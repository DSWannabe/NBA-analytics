import hashlib

from peewee import (
    BigIntegerField,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
    PostgresqlDatabase,
    DecimalField
)

db = PostgresqlDatabase("postgresql://postgres:postgres@localhost:5432/nba_data")

class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False

class NbaTeamInfo(BaseModel):
    team_name_full = CharField(unique=True)
    team = CharField(primary_key=True)

class NbaPlayerInfo(BaseModel):
    player = CharField(max_length=100, primary_key=True)
    birth = DateField()
    height = DecimalField(max_digits=4, decimal_places=2, null=True)
    weight = DecimalField(max_digits=4, decimal_places=2, null=True)
    country = CharField(max_length=100, null=True)
    draft = CharField(max_length=100, null=True)

# class DateTable(BaseModel):
#     date = DateField(primary_key=True)

class NbaPlayerGameStats(BaseModel):
    player = CharField(max_length=100, null=True)
    team = CharField(max_length=100, null=True)
    matchup = CharField(max_length=100, null=True)
    game_date = DateField(null=True)
    w_l = CharField(max_length=10, null=True)
    min = FloatField(null=True)
    pts = FloatField(null=True)
    fgm = FloatField(null=True)
    fga = FloatField(null=True)
    fg_pct = CharField(null=True)
    three_pm = FloatField(null=True)
    three_pa = FloatField(null=True)
    three_ppct = FloatField(null=True)
    ftm = FloatField(null=True)
    fta = FloatField(null=True)
    ft_pct = CharField(max_length=10, null=True)
    oreb = FloatField(null=True)
    dreb = FloatField(null=True)
    reb = FloatField(null=True)
    ast = FloatField(null=True)
    stl = FloatField(null=True)
    blk = FloatField(null=True)
    tov = FloatField(null=True)
    pf = FloatField(null=True)
    plus_minus_box = FloatField(null=True)
    fp = FloatField(null=True)

class NbaPlayerSeasonalStats(BaseModel):
    player = CharField(max_length=100, null=True)
    team = CharField(max_length=100, null=True)
    games_played = IntegerField(null=True)
    wins = IntegerField(null=True)
    losses = IntegerField(null=True)
    minutes = FloatField(null=True)
    points = FloatField(null=True)
    fgm = FloatField(null=True)
    fga = FloatField(null=True)
    fgp = FloatField(null=True)
    three_pm = FloatField(null=True)
    three_pa = FloatField(null=True)
    three_ppct = FloatField(null=True)
    ftm = FloatField(null=True)
    fta = FloatField(null=True)
    ft_pct = FloatField(null=True)
    oreb = FloatField(null=True)
    dreb = FloatField(null=True)
    reb =  FloatField(null=True)
    ast = FloatField(null=True)
    tov = FloatField(null=True)
    stl = FloatField(null=True)
    blk = FloatField(null=True)
    pf = FloatField(null=True)
    fp = FloatField(null=True)
    dd2 = FloatField(null=True)
    td3 = FloatField(null=True)
    plus_minus_box = FloatField(null=True)

def create_table():
    with db:
        db.create_tables(
            [
                NbaPlayerGameStats,
                NbaPlayerSeasonalStats,
                NbaTeamInfo,
                NbaPlayerInfo
            ]
        )

if __name__ == "__main__":
    create_table()


