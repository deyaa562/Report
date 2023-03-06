from time import time


def timestamp():
    return str(int(time() * 1000))

class Data:
    endpoint = ''
    launch_name = ''
    uuid = ''
    project = ''
    headers = {
        'Authorization': f'Bearer {uuid}'
    }

    base_item_data = {
       'name': 'My Test Suite',
       'type': 'suite',
       'start_time': timestamp(),
       'launchUuid': ''
    }

    @classmethod
    def update_url(cls):
        cls.endpoint = f'{cls.endpoint}/api/v1/{cls.project}'
        cls.update_headers()

    @classmethod
    def update_headers(cls):
        cls.headers = {
            'Authorization': f'Bearer {cls.uuid}'}

def parse():
    import configparser
    import os

    filename = 'report_properties.ini'
    for root, dirs, files in os.walk('.'):
        if filename in files:
            # The file was found
            filepath = os.path.join(root, filename)
    # The root directory of the project is the parent directory of the directory containing 'requirements.txt'
    config = configparser.ConfigParser()
    config.read(filepath)
    endpoint = config.get('Data', 'endpoint')
    uuid = config.get('Data', 'uuid')
    launch_name = config.get('Data', 'launch_name')
    project = config.get('Data', 'project')
    Data.endpoint = endpoint
    Data.uuid = uuid
    Data.launch_name = launch_name
    Data.project = project
    Data.update_url()

parse()
