import requests
import json
import os
import inspect
from ._data import timestamp, Data, parse
from typing import Union


class Launch:
    items = {'': ''}

    @classmethod
    def get_enclosing_class_name(cls, func):
        '''
        Get the name of the enclosing class for a function.
        Returns None if the function is not a method.
        '''
        if inspect.ismethod(func) or inspect.isfunction(func):
            # Get the name of the first argument
            arg_names = inspect.getfullargspec(func).args
            if arg_names and arg_names[0] == 'self':
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
            f'startTime': timestamp()}

        if Data.base_item_data['launchUuid'] == '':
            respone = requests.post(url=f'{Data.endpoint}/launch', headers=Data.headers, json=data)
            print(respone.json())
            launch_uuid = respone.json()['id']
            Data.base_item_data['launchUuid'] = launch_uuid

        else:
            print('Second attemp to start a launch')

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
        parent = cls.items[parent_item]
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
    def finish_item(cls, item_name: str):
        item = cls.items[item_name]
        json_data= {
            'launchUuid': Data.base_item_data['launchUuid'],
            'endTime': timestamp()}

        requests.put(url=f'{Data.endpoint}/item/{item}', headers=Data.headers, json=json_data)
        cls.items.pop(item_name)

    @classmethod
    def finish_passed_item(cls, item_name: str):
        item = cls.items[item_name]
        json_data= {
            'launchUuid': Data.base_item_data['launchUuid'],
            'endTime': timestamp(),
            'status': 'passed'}

        response = requests.put(url=f'{Data.endpoint}/item/{item}', headers=Data.headers, json=json_data)
        cls.items.pop(item_name)

    @classmethod
    def finish_failed_item(cls, item_name: str, reason):
        item = cls.items[item_name]
        json_data = {
            'launchUuid': Data.base_item_data['launchUuid'],
            'endTime': timestamp(),
            'status': 'failed',
            'issue': {'comment': reason}}

        requests.put(url=f'{Data.endpoint}/item/{item}', headers=Data.headers, json=json_data)
        cls.items.pop(item_name)

    @classmethod
    def create_log(cls, item: str, message: str, level: str = "INFO"):
        json_data = {
            "launchUuid": Data.base_item_data['launchUuid'],
            "itemUuid": cls.items[item],
            "time": timestamp(),
            "message": message,
            "level": level,
        }

        requests.post(url=f'{Data.endpoint}/log', headers=Data.headers, json=json_data)

    @classmethod
    def add_attachment(cls, item: str, message: str, level: str, attachment: Union[str, bytes], attachment_type: str):
        file_name = os.path.basename(attachment)
        json_body = {
            "launchUuid": Data.base_item_data['launchUuid'],
            "time": timestamp(),
            "message": message,
            "level": level,
            "itemUuid": cls.items[item],
            "file": {"name": file_name}}

        data = b''
        data += b'--boundary-string\r\n'
        data += f'Content-Disposition: form-data; name="json_request_part"\r\n'.encode('utf-8')
        data += b'Content-Type: application/json\r\n\r\n'
        data += attachment if type(attachment) is bytes else json.dumps([json_body]).encode('utf-8')
        data += b'\r\n--boundary-string\r\n'
        data += f'Content-Disposition: form-data; name="{file_name}"; filename="Screenshot.png"\r\n'.encode('utf-8')
        data += f'Content-Type: {attachment_type}\r\n\r\n'.encode('utf-8')
        with open('Screenshot.png', 'rb') as f:
            image_data = f.read()
        data += image_data
        data += b'\r\n--boundary-string--\r\n'
        headers = Data.headers
        headers['Content-Type'] = 'multipart/form-data; boundary=boundary-string'
        requests.post(url=f'{Data.endpoint}/log', headers=headers, data=data)
