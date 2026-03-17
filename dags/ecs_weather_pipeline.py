from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from datetime import datetime

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026,3,12),
    schedule="30 17 * * *",
    catchup=False,
) as dag:
    task1 = EcsRunTaskOperator(
        task_id="run_weather_pipeline",
        cluster="weather-pipeline-cluster",
        task_definition="weather-pipeline-task",
        launch_type="FARGATE",
        overrides={},
        network_configuration={
            "awsvpcConfiguration": {
                "subnets": [
                    "subnet-a90e3597",
                    "subnet-55629633"
                ],
                "securityGroups": ["sg-a5ce2e8b"],
                "assignPublicIp": "ENABLED"
            }
        }
    )