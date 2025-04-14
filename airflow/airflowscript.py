from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from NBA.spiders.player_game_stats import player_game_stats

dag = DAG(
    'anhtu_dag01',
    default_args={
        'email': ['tuphamanh19992022@gmail.com'],
        'email_on_failure': True,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Anhtu DAG 01',
    schedule_interval=timedelta(days=30),
    start_date=datetime(2025, 4, 20),
    tags=['anhtu_nbadag']
)