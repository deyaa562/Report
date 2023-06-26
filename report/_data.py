import json
from time import time


LAUNCH_DATA_FILE = './launch_data.json'

with open(LAUNCH_DATA_FILE, 'w') as file:
    file.write(r'{"launchUuid": ""}')

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

    @classmethod
    def read_data_file(cls):
        with open(LAUNCH_DATA_FILE, 'r') as file:
            data = json.load(file)
            cls.base_item_data['launchUuid'] = data['launchUuid']

    @classmethod
    def update_data_file(cls, new_uuid):
        cls.read_data_file()
        cls.base_item_data['launchUuid'] = new_uuid
        with open(LAUNCH_DATA_FILE, 'w') as file:
            json.dump(cls.base_item_data, file)
            
def parse():
    import configparser
    import os

    filename = 'report_properties.ini'
    config = configparser.ConfigParser()
    for root, dirs, files in os.walk('.'):
        if filename in files:
            filepath = os.path.join(root, filename)
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
