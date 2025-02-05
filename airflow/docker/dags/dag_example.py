from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'anhtupham99',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id="dag1_v5",
    default_args=default_args,
    description="First dag we write",
    start_date=datetime(2021, 7, 29, 2),
    schedule_interval='@daily',
) as dag:
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo hello world, this is the first task!"
    )

    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo I am the second task, I run after the first task"
    )

    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo I am the third task, I run after the task 1, at the same time with task 2"
    )

    # dependency method 1
    # task1.set_downstream(task2) # dependency: task1 runs first then task2 is allowed to run
    # task1.set_downstream(task3) # dependency: task1 runs first then task3 is allowed to run

    # dependency method 2
    # task1 >> task2
    # task1 >> task3

    # dependency method 3
    task1 >> [task2, task3]