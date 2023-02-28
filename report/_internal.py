from time import time
import requests
import inspect
from ._config import UUID, PROJECT

def timestamp():
    return str(int(time() * 1000))


BASE_URL = f'http://localhost:8080/api/v1/{PROJECT}'

headers = {
    'Authorization': f'Bearer {UUID}'
}

base_item_data = {
   'name': 'My Test Suite',
   'type': 'suite',
   'start_time': timestamp(),
   'launchUuid': ''
}

items = {'': ''}


def get_enclosing_class_name(func):
    '''
    Get the name of the enclosing class for a function.
    Returns None if the function is not a method.
    '''
    if inspect.ismethod(func) or inspect.isfunction(func):
        # Get the name of the first argument
        arg_names = inspect.getfullargspec(func).args
        if arg_names and arg_names[0] == 'self':
            # The first argument is 'self', so this is a method
            return func.__qualname__.split('.')[0]
    return None


def get_caller_name():
    frame = inspect.currentframe()
    caller_frame = frame.f_back.f_back
    return caller_frame.f_code.co_name

def start_launch(name: str = 'New Launch'):
    data = {
        'name': name,
        'description': 'My first launch on RP',
        f'startTime': timestamp()}
    
    if base_item_data['launchUuid'] == '':
        respone = requests.post(url=f'{BASE_URL}/launch', headers=headers, json=data)
        print(respone.json())
        launch_uuid = respone.json()['id']
        base_item_data['launchUuid'] = launch_uuid
    
    else:
        print('Second attemp to start a launch')

def finish_launch():
    import time
    time.sleep(20)
    requests.put(url=f'{BASE_URL}/launch/{base_item_data["launchUuid"]}/finish', headers=headers, json={'endTime': timestamp()})

# def log(parent: str, message: str):
     
#     data = {'[{\
#         "itemUuid":"{0}",\
#         "launchUuid":"{1}",\
#         "time":"{2}",\
#         "message":"Some critical exception",\
#         "level":40000,\
#         "file":{"name":"Untitled.png"}}'.format(parent, base_item_data['launchUuid'], timestamp())
#     }
#     payload = {f'[{data}]'}
#     files=[

#     ]
#     headers = {
#       'Content-Type': 'application/json',
#       'Authorization': 'Bearer 039eda00-b397-4a6b-bab1-b1a9a90376d1'
#     }

#     response = requests.request("POST", url=f'{BASE_URL}/log', headers=headers, data=payload, files=files)
#     data = {
#         'launchUuid': base_item_data['launchUuid'],
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
#     response = requests.post(url=f'{BASE_URL}/log', headers=headers, files={'file': png_data, 'json_request_part': json_request_part})
#     print(response.json())

def create_report_item(
        name: str,
        parent_item: str = '', 
        type: str = '',  
        description: str = '', 
        has_stats: bool = True):

    parent = items[parent_item]
    data = base_item_data
    data['name'] = name
    data['type'] = type
    data['start_time'] = timestamp()
    data['description'] = description
    data['hasStats'] = has_stats

    response = requests.post(url=f'{BASE_URL}/item/{parent}', headers=headers, json=data)
    response_json = response.json()
    print(f'{name} + {response_json}')
    return response_json['id']


def finish_item(item_name: str):
    item = items[item_name]
    json_data= {
        'launchUuid': base_item_data['launchUuid'],
        'endTime': timestamp()
    }
    requests.put(url=f'{BASE_URL}/item/{item}', headers=headers, json=json_data)

def finish_passed_item(item_name: str):
    item = items[item_name]
    json_data= {
        'launchUuid': base_item_data['launchUuid'],
        'endTime': timestamp(),
        'status': 'passed'
    }
    requests.put(url=f'{BASE_URL}/item/{item}', headers=headers, json=json_data)

def finish_failed_item(item_name: str, reason):
    item = items[item_name]
    print('finished ' + item_name)
    json_data= {
        'launchUuid': base_item_data['launchUuid'],
        'endTime': timestamp(),
        'status': 'failed',
        'issue': {'comment': reason}
        }
    
    requests.put(url=f'{BASE_URL}/item/{item}', headers=headers, json=json_data)