from prefect import flow, task
from prefect.deployments import Deployment
from prefect import get_run_logger
import requests
import uuid
from prefect.filesystems import GitHub

API_COCKPIT_SCHEDULER_URL = 'http://localhost:8888'


github_block = GitHub.load("test1")
# app is in vehicleslabs folder in github repo test1 
github_block.get_directory("vehicleslabs")

# github_block = GitHub(repo="test1", directory="vehicleslabs")




@flow
def API_CockpitSchedulers():
    @task
    def hello_world():
        logger = get_run_logger()
        logger.info("Hello World!")
    hello_world()
    

deployments = [
    Deployment.build_from_flow(
        flow=API_CockpitSchedulers,
        name="API_CockpitScheduler",
         storage=github_block,
         path="."

        # schedule=CronSchedule(
        #     cron="0 0 * * *",
        # ),
    ),

    
]


def main():
    for deployment in deployments:
        deployment.apply()


if __name__ == "__main__":
    main()

    # docker run -p 8080:8080 my-prefect-server
    # docker run -p 4200:4200 --name my-prefect-container my-prefect-image
