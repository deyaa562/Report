import requests
import inspect
from ._data import timestamp, Data, parse

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
            'description': 'My first launch on RP',
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
        print(Data.endpoint)
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

    @classmethod
    def finish_passed_item(cls, item_name: str):
        item = cls.items[item_name]
        json_data= {
            'launchUuid': Data.base_item_data['launchUuid'],
            'endTime': timestamp(),
            'status': 'passed'
        }
        requests.put(url=f'{Data.endpoint}/item/{item}', headers=Data.headers, json=json_data)

    @classmethod
    def finish_failed_item(cls, item_name: str, reason):
        item = cls.items[item_name]
        json_data = {
            'launchUuid': Data.base_item_data['launchUuid'],
            'endTime': timestamp(),
            'status': 'failed',
            'issue': {'comment': reason}
            }

        requests.put(url=f'{Data.endpoint}/item/{item}', headers=Data.headers, json=json_data)

    @classmethod
    def create_log(cls, item: str, message: str, level: str = "INFO"):
        json_data = {
            "launchUuid": Data.base_item_data['launchUuid'],
            "itemUuid": cls.items[item],
            "time": timestamp(),
            "message": message,
            "level": level,
        }

        response = requests.post(url=f'{Data.endpoint}/log', headers=Data.headers, json=json_data)

    # @classmethod
    # def add_attachment(cls, name: str, item: str, file_path: str):
    #     import os
    #     file_name = os.path.basename(file_path)
    #     body = {
    #         "launchUuid": Data.base_item_data['launchUuid'],
    #         "itemUuid": cls.items[item],
    #         "time": timestamp(),
    #         "message": cls.items[item],
    #         "level": 40000,
    #         "file":{
    #           "name": file_name
    #         },
    #     }

    #     json_file_path = '/tmp/json_file.json'
    #     with open(json_file_path, 'w') as file:
    #         file.write(json.dumps([body]))

    #     payload = {"json_request_part": f'{json.dumps([body])};type=application/json'}
    #     print(payload)
    #     files = {'file': (file_name ,open(file_path,'rb'), 'image/png')}

    #     data = f"json_request_part='{json.dumps([body])};type=application/json'"

    #     files = {
    #         ('file', open(file_path, 'rb'), 'image/png'),
    #         ('json_request_part', open(json_file_path, 'r'), 'application/json')
    #     }

    #     response = requests.post(url=f'{Data.endpoint}/log', headers=Data.headers, data=files)
    #     print(response.json())

    # def add_attachment(cls, item: str, file_path: str):
    #     json_data = {
    #         "launchUuid": Data.base_item_data['launchUuid'],
    #         "itemUuid": cls.items[item],
    #         "time": timestamp(),
    #         "message": cls.items[item],
    #         "level": 40000,
    #     }

    #     with open(file_path, 'r') as f:
    #         file_data = f.read()

    #     # Construct the multipart/form-data request
    #     data = (
    #         '--' + '---------------------------1234567890' + '\r\n' +
    #         'Content-Disposition: form-data; name="json_request_part"' + '\r\n' +
    #         'Content-Type: application/json' + '\r\n\r\n' +
    #         json.dumps(json_data) + '\r\n' +
    #         '--' + '---------------------------1234567890' + '\r\n' +
    #         'Content-Disposition: form-data; name="file"; filename="' + file_path + '"' + '\r\n' +
    #         'Content-Type: text/plain' + '\r\n\r\n' +
    #         file_data + '\r\n' +
    #         '--' + '---------------------------1234567890--'
    #     )

    #     # Send the API request
    #     headers = Data.headers
    #     headers['Content-Type'] = 'multipart/form-data; boundary=---------------------------1234567890'
    #     response = requests.post(url=f'{Data.endpoint}/log', headers=headers, data=data)

    #     print(response.status_code)
    #     print(response.text)


