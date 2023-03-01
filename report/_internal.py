from time import time
import requests
import inspect

def timestamp():
    return str(int(time() * 1000))


class Data:
    endpoint = ''
    launch_name = ''
    uuid = ''
    project = ''

    @classmethod
    def update_url(cls):
        cls.endpoint = f'{cls.endpoint}/api/v1/{cls.project}'
        Launch.__update_headers()

    @classmethod
    def parse(cls):
        import configparser
        import os

        # Get the absolute path of the current file
        current_file_path = os.path.abspath(__file__)

        # Get the directory containing the current file
        current_dir = os.path.dirname(current_file_path)

        # Traverse up the directory hierarchy until we find a directory containing a file named 'requirements.txt'
        while not os.path.exists(os.path.join(current_dir, 'requirements.txt')):
            current_dir = os.path.dirname(current_dir)

        # The root directory of the project is the parent directory of the directory containing 'requirements.txt'
        root_dir = os.path.dirname(current_dir)
        config = configparser.ConfigParser()
        config.read(f'{root_dir}/config.ini')

        endpoint = config.get('Data', 'endpoint')
        uuid = config.get('Data', 'uuid')
        launch_name = config.get('Data', 'launch_name')
        project = config.get('Data', 'project')

        Data.endpoint = endpoint
        Data.uuid = uuid
        Data.launch_name = launch_name 
        Data.project = project
        Data.update_url()

class Launch:
    headers = {
        'Authorization': f'Bearer {Data.uuid}'
    }

    base_item_data = {
       'name': 'My Test Suite',
       'type': 'suite',
       'start_time': timestamp(),
       'launchUuid': ''
    }

    items = {'': ''}

    @classmethod
    def __update_headers(cls):
        cls.headers = {
            'Authorization': f'Bearer {Data.uuid}'}
    @classmethod
    def __get_enclosing_class_name(cls, func):
        '''
        Get the name of the enclosing class for a function.
        Returns None if the function is not a method.
        '''
        if inspect.ismethod(func) or inspect.isfunction(func):
            # Get the name of the first argument
            arg_names = inspect.getfullargspec(func).args
            if arg_names and arg_names[0] == 'cls':
                # The first argument is 'cls', so this is a method
                return func.__qualname__.split('.')[0]
        return None

    
    @classmethod
    def get_caller_name(cls):
        frame = inspect.currentframe()
        caller_frame = frame.f_back.f_back
        return caller_frame.f_code.co_name
    
    @classmethod
    def start_launch(cls):

        data = {
            'name': Data.launch_name,
            'description': 'My first launch on RP',
            f'startTime': timestamp()}

        if cls.base_item_data['launchUuid'] == '':
            respone = requests.post(url=f'{Data.endpoint}/launch', headers=cls.headers, json=data)
            print(respone.json())
            launch_uuid = respone.json()['id']
            cls.base_item_data['launchUuid'] = launch_uuid

        else:
            print('Second attemp to start a launch')
    
    @classmethod
    def finish_launch(cls):
        requests.put(url=f'{Data.endpoint}/launch/{cls.base_item_data["launchUuid"]}/finish', headers=cls.headers, json={'endTime': timestamp()})

    # def log(parent: str, message: str):

    #     data = {'[{\
    #         "itemUuid":"{0}",\
    #         "launchUuid":"{1}",\
    #         "time":"{2}",\
    #         "message":"Some critical exception",\
    #         "level":40000,\
    #         "file":{"name":"Untitled.png"}}'.format(parent, cls.base_item_data['launchUuid'], timestamp())
    #     }
    #     payload = {f'[{data}]'}
    #     files=[

    #     ]
    #     headers = {
    #       'Content-Type': 'application/json',
    #       'Authorization': 'Bearer 039eda00-b397-4a6b-bab1-b1a9a90376d1'
    #     }

    #     response = requests.request("POST", url=f'{Data.endpoint}/log', headers=headers, data=payload, files=files)
    #     data = {
    #         'launchUuid': cls.base_item_data['launchUuid'],
    #         'itemUuid': parent,
    #         'time': timestamp(),
    #         'message': message,
    #         'level': 4000,
    #         'file': {'name': 'Untitle.png'}
    #     }
    #     with open('./Untitled.png', mode='rb') as f:
    #         png_data = f.read()

    #     headers = headers
    #     print(headers)
    #     payload = {
    #     'file': ('image.png', png_data, 'image/png'),
    #     'json_data': (None, json.dumps(data), 'application/json')}
    #     json_request_part = ('json_request_part', json.dumps(data), 'application/json')
    #     response = requests.post(url=f'{Data.endpoint}/log', headers=headers, files={'file': png_data, 'json_request_part': json_request_part})
    #     print(response.json())
    
    @classmethod
    def create_report_item(
            cls,
            name: str,
            parent_item: str = '', 
            type: str = '',  
            description: str = '', 
            has_stats: bool = True):

        parent = cls.items[parent_item]
        data = cls.base_item_data
        data['name'] = name
        data['type'] = type
        data['start_time'] = timestamp()
        data['description'] = description
        data['hasStats'] = has_stats

        response = requests.post(url=f'{Data.endpoint}/item/{parent}', headers=cls.headers, json=data)
        response_json = response.json()
        print(f'{name} + {response_json}')
        return response_json['id']

    @classmethod
    def finish_item(cls, item_name: str):
        item = cls.items[item_name]
        json_data= {
            'launchUuid': cls.base_item_data['launchUuid'],
            'endTime': timestamp()
        }
        requests.put(url=f'{Data.endpoint}/item/{item}', headers=cls.headers, json=json_data)
    
    @classmethod
    def finish_passed_item(cls, item_name: str):
        item = cls.items[item_name]
        json_data= {
            'launchUuid': cls.base_item_data['launchUuid'],
            'endTime': timestamp(),
            'status': 'passed'
        }
        requests.put(url=f'{Data.endpoint}/item/{item}', headers=cls.headers, json=json_data)
    
    @classmethod
    def finish_failed_item(cls, item_name: str, reason):
        item = cls.items[item_name]
        print('finished ' + item_name)
        json_data= {
            'launchUuid': cls.base_item_data['launchUuid'],
            'endTime': timestamp(),
            'status': 'failed',
            'issue': {'comment': reason}
            }

        requests.put(url=f'{Data.endpoint}/item/{item}', headers=cls.headers, json=json_data)