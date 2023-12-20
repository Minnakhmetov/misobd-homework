from datetime import timedelta, datetime
import airflow
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator

default_args = {
            'owner': 'airflow',
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'start_date': '2023-12-05',
            'retries': 1,
            'retry_delay': timedelta(minutes=6000),
            'catchup': False
}

dag = DAG(dag_id='testing_stuff',
          default_args=default_args,
          schedule_interval='50 * * * *',
          dagrun_timeout=timedelta(seconds=120))

t1_bash = """
curl -o out_file.zip 'https://www.kaggle.com/datasets/arevel/chess-games'
"""
t2_bash = "unzip -o out_file.zip"

t3_bash = """export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/hadoop/bin:/usr/local/hadoop/sbin:/usr/local/hadoop/sbin" && hdfs dfs -put chess_games.csv /user/hadoop/from_airflow"""

t4_bash = "echo 'Hello world!'"

t5_bash = "rm out_file.zip"
t6_bash = "rm chess_games.csv"
t7_bash = "hdfs dfs -rm /user/hadoop/from_airflow/chess_games.csv"

t1 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='get_dataset_from_web',
                 command=t1_bash,
                 dag=dag)

t2 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='unpack_archive',
                 command=t2_bash,
                 cmd_timeout=300,
                 dag=dag)

t3 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='load_to_hdfs',
                 command=t3_bash,
                 cmd_timeout=300,
                 dag=dag)

t4 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='run_mr_job',
                 command=t4_bash,
                 dag=dag)

t5 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='delete_archive',
                 command=t5_bash,
                 dag=dag)


t6 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='delete_csv',
                 command=t6_bash,
                 dag=dag)


t7 = SSHOperator(ssh_conn_id='ssh_default',
                 task_id='delete_csv_hdfs',
                 command=t7_bash,
                 dag=dag)

t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7