import requests
from . import _internal
import json

def start_launch(name: str = 'New Launch'):
    data = {
        'name': 'test',
        'description': 'My first launch on RP',
        f'startTime': _internal.timestamp()}
    
    if _internal.base_item_data['launchUuid'] == '':
        respone = requests.post(url=f'{_internal.BASE_URL}/launch', headers=_internal.headers, json=data)
        launch_uuid = respone.json()['id']
        _internal.base_item_data['launchUuid'] = launch_uuid
    
    else:
        print('Second attemp to start a launch')

def finish_launch():
    import time
    time.sleep(20)
    requests.put(url=f'{_internal.BASE_URL}/launch/{_internal.base_item_data["launchUuid"]}/finish', headers=_internal.headers, json={'endTime': _internal.timestamp()})

def log(parent: str, message: str):
     
    data = {'[{\
        "itemUuid":"{0}",\
        "launchUuid":"{1}",\
        "time":"{2}",\
        "message":"Some critical exception",\
        "level":40000,\
        "file":{"name":"Untitled.png"}}'.format(parent, _internal.base_item_data['launchUuid'], _internal.timestamp())
    }
    payload = {f'[{data}]'}
    files=[

    ]
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer 039eda00-b397-4a6b-bab1-b1a9a90376d1'
    }

    response = requests.request("POST", url=f'{_internal.BASE_URL}/log', headers=headers, data=payload, files=files)
    data = {
        'launchUuid': _internal.base_item_data['launchUuid'],
        'itemUuid': parent,
        'time': _internal.timestamp(),
        'message': message,
        'level': 4000,
        'file': {'name': 'Untitle.png'}
    }
    with open('./Untitled.png', mode='rb') as f:
        png_data = f.read()
    
    headers = _internal.headers
    print(headers)
    payload = {
    'file': ('image.png', png_data, 'image/png'),
    'json_data': (None, json.dumps(data), 'application/json')}
    json_request_part = ('json_request_part', json.dumps(data), 'application/json')
    response = requests.post(url=f'{_internal.BASE_URL}/log', headers=headers, files={'file': png_data, 'json_request_part': json_request_part})
    print(response.json())

def create_report_item(
        name: str,
        parent_item: str = '', 
        type: str = '',  
        description: str = '', 
        has_stats: bool = True):

    parent = _internal.items[parent_item]
    data = _internal.base_item_data
    data['name'] = name
    data['type'] = type
    data['start_time'] = _internal.timestamp()
    data['description'] = description
    data['hasStats'] = has_stats

    response = requests.post(url=f'{_internal.BASE_URL}/item/{parent}', headers=_internal.headers, json=data)
    response_json = response.json()
    print(f'{name} + {response_json}')
    return response_json['id']


def finish_item(item_name: str):
    item = _internal.items[item_name]
    json_data= {
        'launchUuid': _internal.base_item_data['launchUuid'],
        'endTime': _internal.timestamp()
    }
    requests.put(url=f'{_internal.BASE_URL}/item/{item}', headers=_internal.headers, json=json_data)

def finish_passed_item(item_name: str):
    item = _internal.items[item_name]
    json_data= {
        'launchUuid': _internal.base_item_data['launchUuid'],
        'endTime': _internal.timestamp(),
        'status': 'passed'
    }
    requests.put(url=f'{_internal.BASE_URL}/item/{item}', headers=_internal.headers, json=json_data)

def finish_failed_item(item_name: str, reason):
    item = _internal.items[item_name]
    print('finished ' + item_name)
    json_data= {
        'launchUuid': _internal.base_item_data['launchUuid'],
        'endTime': _internal.timestamp(),
        'status': 'failed',
        'issue': {'comment': reason}
        }
    
    requests.put(url=f'{_internal.BASE_URL}/item/{item}', headers=_internal.headers, json=json_data)

def step(name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            parent = _internal.get_caller_name()
            item_id = create_report_item(
                name=name,
                parent_item=parent,
                type='step',
                has_stats=False,
                description=func.__doc__)

            _internal.items[func.__name__] = item_id
            result = None
            try:
                result = func(*args, **kwargs)
            
            except Exception as exception:
                finish_failed_item(func.__name__, str(exception))
                raise exception

            finish_passed_item(func.__name__)
            return result

        return wrapper
    return decorator

def title(name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            item_id = create_report_item(
                name=name,
                parent_item=_internal.get_enclosing_class_name(func),
                type='test',
                description=func.__doc__)

            _internal.items[func.__name__] = item_id
            result = None
            log(func.__name__, 'test')

            result = func(*args, **kwargs)
            
            finish_item(func.__name__)
            return result

        return wrapper
    return decorator

def feature(name: str):
    def decorator(cls):
        item_id = create_report_item(
            name=name,
            type='suite',
            description=cls.__doc__)

        _internal.items[cls.__name__] = item_id
        return cls

    return decorator

def story(name: str):
    def decorator(cls):

        parent = cls.__mro__[1].__name__
        item_id = create_report_item(
            name=name,
            parent_item=parent,
            type='story',
            description=cls.__doc__)

        _internal.items[cls.__name__] = item_id
        return cls

    return decorator


