from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from NBA.spiders.player_game_stats import GameStats
from NBA.spiders.game_results import GameResults
from NBA.spiders.player_info import PlayerInfo
from NBA.spiders.player_urls import PlayerURL
from NBA.spiders.player_seasonal_stats import SeasonalStats
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import logging

logger = logging.getLogger(__name__)

def run_spider():
    settings = get_project_settings()
    spiders = [PlayerURL, PlayerInfo, GameStats, SeasonalStats, GameResults] 
    for spider in spiders:
        process = CrawlerProcess(settings)
        process.crawl(spider)
        process.start()  # the script will block here until the crawling is finished

with DAG(
    'anhtu_dag01',
    default_args={
        'owner': 'anhtu',
        'email': ['tuphamanh19992022@gmail.com'],
        'email_on_failure': True,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Anhtu DAG 01',
    schedule_interval=timedelta(days=30),
    start_date=datetime(2025, 4, 15),
    catchup=False,
    tags=['anhtu_nbadag'],
) as dag:
    run_spiders = PythonOperator(
        task_id='run_spiders',
        python_callable=run_spider
    )

    spider_task1 = PythonOperator(
        task_id='run_spider1',
        python_callable=run_spider,
        op_kwargs={'spider_class': PlayerURL},
        provide_context=True # Pass Airflow context to function
    )

    spider_task2 = PythonOperator(
        task_id='run_spider2',
        python_callable=run_spider,
        op_kwargs={'spider_class': PlayerInfo},
        provide_context=True # Pass Airflow context to function
    )

    spider_task3 = PythonOperator(
        task_id='run_spider3',
        python_callable=run_spider,
        op_kwargs={'spider_class': GameStats},
        provide_context=True # Pass Airflow context to function
    )

    spider_task4 = PythonOperator(
        task_id='run_spider4',
        python_callable=run_spider,
        op_kwargs={'spider_class': SeasonalStats},
        provide_context=True # Pass Airflow context to function
    )

    spider_task5 = PythonOperator(
        task_id='run_spider5',
        python_callable=run_spider,
        op_kwargs={'spider_class': GameResults},
        provide_context=True # Pass Airflow context to function
    )

    run_spiders >> [spider_task1, spider_task2, spider_task3, spider_task4, spider_task5]