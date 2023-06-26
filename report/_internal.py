import requests
import json
import os
import inspect
import json
from ._data import timestamp, Data, parse
import tempfile

temp_dir = tempfile.gettempdir()
FILE_PATH = os.path.join(temp_dir, 'test.json')
with open(FILE_PATH, 'w') as file:
    file.write(r'{"": ""}')


class Launch:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_enclosing_class_name(cls, func):
        '''
        Get the name of the enclosing class for a function.
        Returns None if the function is not a method.
        '''
        if inspect.ismethod(func) or inspect.isfunction(func):
            arg_names = inspect.getfullargspec(func).args
            if arg_names and arg_names[0] == 'self':
                return func.__qualname__.split('.')[0]
        return None

    @classmethod
    def items(cls) -> dict:
        with open(FILE_PATH, 'r') as file:
            return json.load(file)

    @classmethod
    def __update_items_file(cls, new_items: dict):
        with open(FILE_PATH, 'w') as file:
            json.dump(new_items, file)
    
    @classmethod
    def add_item(cls, item_name, item_id):
        current_items = cls.items()
        current_items[item_name] = item_id
        Launch.__update_items_file(current_items)
    
    @classmethod
    def get_latest_item(cls):
        current_items = cls.items()
        last_key, _ = list(current_items.items())[-1]
        return last_key

    @classmethod
    def delete_item(cls, item_name):
        current_items = cls.items()
        current_items.pop(item_name, None)
        Launch.__update_items_file(current_items)

    @classmethod
    def get_caller_name(cls):
        frame = inspect.currentframe()
        caller_frame = frame.f_back.f_back
        return caller_frame.f_code.co_name

    @classmethod
    def start_launch(cls):

        data = {
            'name': Data.launch_name,
            f'startTime': timestamp()}

        Data.read_data_file()
        if Data.base_item_data['launchUuid'] == '':
            respone = requests.post(url=f'{Data.endpoint}/launch', headers=Data.headers, json=data)
            launch_uuid = respone.json()['id']
            Data.update_data_file(launch_uuid)


    @classmethod
    def finish_launch(cls):
        requests.put(url=f'{Data.endpoint}/launch/{Data.base_item_data["launchUuid"]}/finish', headers=Data.headers, json={'endTime': timestamp()})


    @classmethod
    def create_report_item(
            cls,
            name: str,
            parent_item: str = '',
            type: str = '',
            description: str = '',
            has_stats: bool = True):

        parse()
        current_items = cls.items()
        parent = current_items[parent_item]
        if Data.base_item_data['launchUuid'] == '':
            Data.read_data_file()

        data = Data.base_item_data
        data['name'] = name
        data['type'] = type
        data['start_time'] = timestamp()
        data['description'] = description
        data['hasStats'] = has_stats

        response = requests.post(url=f'{Data.endpoint}/item/{parent}', headers=Data.headers, json=data)
        response_json = response.json()
        return response_json['id']

    @classmethod
    def finish_item(cls, item_name: str, passed: bool = True):
        status = 'passed' if passed else 'failed'
        current_items = cls.items()
        try:
            item = current_items[item_name]
            json_data= {
            'launchUuid': Data.base_item_data['launchUuid'],
            'endTime': timestamp(),
            'status': status}
            data = Data.headers
            data['Content-Type']='application/json'
            response = requests.put(url=f'{Data.endpoint}/item/{item}', headers=data, json=json_data)
            cls.delete_item(item_name)
        except:
            pass


    @classmethod
    def finish_passed_item(cls, item_name: str):
        current_items = cls.items()
        item = current_items[item_name]
        json_data= {
            'launchUuid': Data.base_item_data['launchUuid'],
            'endTime': timestamp(),
            'status': 'passed'}

        response = requests.put(url=f'{Data.endpoint}/item/{item}', headers=Data.headers, json=json_data)
        cls.delete_item(item_name)

    @classmethod
    def finish_failed_item(cls, item_name: str, message: str, reason: str):
        current_items = cls.items()
        item = current_items[item_name]
        json_data = {
            'launchUuid': Data.base_item_data['launchUuid'],
            'endTime': timestamp(),
            'status': 'failed',
            'issue': {
                'issueType': 'pb001',
                'comment': message},
            'description': reason}

        response = requests.put(url=f'{Data.endpoint}/item/{item}', headers=Data.headers, json=json_data)
        cls.delete_item(item_name)

    @classmethod
    def create_log(cls, item: str, message: str, level: str = "INFO"):
        current_items = cls.items()
        json_data = {
            "launchUuid": Data.base_item_data['launchUuid'],
            "itemUuid": current_items[item],
            "time": timestamp(),
            "message": message,
            "level": level,
        }

        requests.post(url=f'{Data.endpoint}/log', headers=Data.headers, json=json_data)

    @classmethod
    def add_attachment(cls, message: str, level: str, attachment: str, attachment_type: str, item: str = ''):
        file_name = os.path.basename(attachment)
        current_items = cls.items()
        item_uuid = current_items[item] if len(item) > 0 else cls.get_latest_item()
        json_body = {
            "launchUuid": Data.base_item_data['launchUuid'],
            "time": timestamp(),
            "message": message,
            "level": level,
            "itemUuid": item_uuid,
            "file": {"name": file_name}}

        data = b''
        data += b'--boundary-string\r\n'
        data += f'Content-Disposition: form-data; name="json_request_part"\r\n'.encode('utf-8')
        data += b'Content-Type: application/json\r\n\r\n'
        data += json.dumps([json_body]).encode('utf-8')
        data += b'\r\n--boundary-string\r\n'
        data += f'Content-Disposition: form-data; name="{file_name}"; filename="Screenshot.png"\r\n'.encode('utf-8')
        data += f'Content-Type: {attachment_type}\r\n\r\n'.encode('utf-8')
        with open(attachment, 'rb') as f:
            image_data = f.read()
        data += image_data
        data += b'\r\n--boundary-string--\r\n'
        headers = Data.headers
        headers['Content-Type'] = 'multipart/form-data; boundary=boundary-string'
        response = requests.post(url=f'{Data.endpoint}/log', headers=headers, data=data)
        return response