from time import time
import inspect

def timestamp():
    return str(int(time() * 1000))


BASE_URL = 'http://localhost:8080/api/v1/rp_project'


headers = {
    'Authorization': 'Bearer 2aa3e90f-2b5e-426e-bc9b-9e257f3ddbbe'
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