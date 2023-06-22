from prefect import flow, task
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from prefect import get_run_logger
import requests
import uuid
import os

API_COCKPIT_SCHEDULER_URL = 'http://localhost:8888'

from prefect.filesystems import GitHub

github_block = GitHub.load("test1")


github_block.get_directory("vehicleslabs")

github_block.save("dev", overwrite=True)
### start of declaration related to fapi_cockpit
@flow
def API_CockpitScheduler():
    url = str(API_COCKPIT_SCHEDULER_URL) + '/get_all_data'
    runing_id = uuid.uuid4()
    response = requests.get(url)
    logger = get_run_logger()
    logger.info(f"runing_id: {runing_id}")
    print(response.json())
    json_data = response.json()
    for data in json_data:
            try:
                if data['api_json'] == 'post':
                    @task
                    def get_output():
                        url = data['swagger_api_name']
                        response = requests.post(url, json=data['input_data_json'])
                        print(response.json())
                        status_api = str(API_COCKPIT_SCHEDULER_URL) + '/scheduler_request'
                        status_data = {
                            'runing_id': str(runing_id),
                            'api_name': data['swagger_api_name'],
                            'status': 'success',
                            'message': 'success',
                            'expected_output_json': data['expected_output_json'],
                            'method': data['api_json'] ,
                            'details' : data['details']
                        }
                        logger.info(f"runing_id: {runing_id}")
                        status_response = requests.post(status_api, json=status_data)
                        print(status_response.json())

                        return response.json()
                    get_output()
                elif data['api_json'] == 'get':
                    @task
                    def get_output():
                        url = data['swagger_api_name']
                        response = requests.get(url)
                        print(response.json())
                        status_api = str(API_COCKPIT_SCHEDULER_URL) + '/scheduler_request'
                        status_data = {
                            'runing_id': str(runing_id),
                            'api_name': data['swagger_api_name'],
                            'status': 'success',
                            'message': 'success',
                            'expected_output_json': data['expected_output_json'],
                            'method': data['api_json'] ,
                            'details' : data['details']
                        }
                        status_response = requests.post(status_api, json=status_data)
                        logger.info(f"runing_id: {runing_id}")
                        logger.info(f"status_response: {status_response.json()}")
                        print(status_response.json())
                        return response.json()
                    get_output()
                elif data['api_json'] == 'put':
                    @task
                    def get_output():
                        url = data['swagger_api_name']
                        response = requests.put(url, json=data['input_data_json'])
                        print(response.json())
                        status_api = str(API_COCKPIT_SCHEDULER_URL) + '/scheduler_request'
                        status_data = {
                            'runing_id': str(runing_id),
                            'api_name': data['swagger_api_name'],
                            'status': 'success',
                            'message': 'success',
                            'expected_output_json': data['expected_output_json'],
                            'method': data['api_json'] ,
                            'details' : data['details']
                        }
                        status_response = requests.post(status_api, json=status_data)
                        logger.info(f"runing_id: {runing_id}")
                        logger.info(f"status_response: {status_response.json()}")

                        print(status_response.json())
                        return response.json()
                    get_output()
                elif data['api_json'] == 'delete':
                    @task
                    def get_output():
                        url = data['swagger_api_name']
                        response = requests.delete(url)
                        print(response.json())
                        status_api = str(API_COCKPIT_SCHEDULER_URL) + '/scheduler_request'
                        status_data = {
                            'runing_id': str(runing_id),
                            'api_name': data['swagger_api_name'],
                            'status': 'success',
                            'message': 'success',
                            'expected_output_json': data['expected_output_json'],
                            'method': data['api_json'] ,
                            'details' : data['details']
                        }
                        status_response = requests.post(status_api, json=status_data)
                        logger.info(f"runing_id: {runing_id}")
                        logger.info(f"status_response: {status_response.json()}")
                        print(status_response.json())
                        return response.json()
                    get_output()
                elif data['api_json'] == 'patch':
                    @task
                    def get_output():
                        url = data['swagger_api_name']
                        response = requests.patch(url, json=data['input_data_json'])
                        print(response.json())
                        status_api = str(API_COCKPIT_SCHEDULER_URL) + '/scheduler_request'
                        status_data = {
                            'runing_id': str(runing_id),
                            'api_name': data['swagger_api_name'],
                            'status': 'success',
                            'message': 'success',
                            'expected_output_json': data['expected_output_json'],
                            'method': data['api_json'] ,
                            'details' : data['details']
                        }

                        status_response = requests.post(status_api, json=status_data)
                        logger.info(f"runing_id: {runing_id}")
                        logger.info(f"status_response: {status_response.json()}")
                        print(status_response.json())
                        return response.json()
                    get_output()
                else:
                    print('No API Found')
            except Exception as e:
                status_api = str(API_COCKPIT_SCHEDULER_URL) + '/scheduler_request'
                status_data = {
                    'runing_id': str(runing_id),
                    'api_name': data['swagger_api_name'],
                    'status': 'failed',
                    'message': str(e),
                    'expected_output_json': data['expected_output_json'] if data['expected_output_json']!=None else {},
                    'method': data['api_json'] ,
                    'details' : data['details']
                }
    
                status_response = requests.post(status_api, json=status_data)
                logger.info(f"runing_id: {runing_id}")
                logger.info(f"status_response: {status_response.json()}")

deployments = [
    Deployment.build_from_flow(
        flow=API_CockpitScheduler,
        name="API_CockpitScheduler",
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
