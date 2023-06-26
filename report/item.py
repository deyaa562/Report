from ._internal import Launch
import functools
from typing import Any, Union, Literal
from .core import *
import traceback


class step:
    def __init__(self, name: str = None):
        self.name = name if name else None

    def __call__(self, func):
        __tracebackhide__ = True
        func.__new_name__ = self.name if self.name else func.__name__
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            __tracebackhide__ = True
            func_is_fixture = _is_fixture(func, args, kwargs)
            if not func_is_fixture:
                caller = Launch.get_caller_name()
                if 'test_' in caller or '_test' in caller:
                    parent = f'{caller}_Execution'
                else:
                    parent = caller

                item_id = Launch.create_report_item(
                    name=self.name,
                    parent_item=parent,
                    type='step',
                    has_stats=False,
                    description=func.__doc__)
    
                Launch.add_item(func.__name__, item_id)

            passed = True
            try:
                result = _run_func(func, *args, **kwargs)
            except:
                passed = False
            
            if not func_is_fixture:
                Launch.finish_item(func.__name__, passed)

            return result

        return wrapper

    def __enter__(self):
        __tracebackhide__ = True
        parent = Launch.get_latest_item()
        item_id = Launch.create_report_item(
                name=self.name,
                parent_item=parent,
                type='step',
                has_stats=False,
                description='')

        Launch.add_item(self.name, item_id)

    def __exit__(self, exc_type, exc_value, tb):
        __tracebackhide__ = True

        passed = exc_type is None
        if passed:
            Launch.finish_item(self.name, passed)

        elif not passed:
            traceback_str = ''.join(traceback.format_tb(tb))
            message = f'{exc_type.__name__}: {exc_value}'
            Launch.finish_failed_item(self.name, message=message, reason=traceback_str)


class title:
    def __init__(self, name: str):
        self.name = name
        
    def __call__(self, func):
        __tracebackhide__ = True
        func.__new_name__ = self.name
        self.__name__ = func.__name__
        self.__qualname__ = func.__qualname__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            __tracebackhide__ = True
            func.formatted_name = self.name.format(*args, **kwargs)
            result = func(*args, **kwargs)
            return result

        return wrapper
    
    def __enter__(self):
        __tracebackhide__ = True
        parent = Launch.get_caller_name()
        item_id = Launch.create_report_item(
                name=self.name,
                parent_item=parent,
                type='step',
                has_stats=False,
                description='')

        Launch.add_item(self.name, item_id)

    def __exit__(self, exc_type, exc_value, tb):
        __tracebackhide__ = True
        passed = exc_type is None
        if passed:
            Launch.finish_item(self.name, passed)

        elif not passed:
            traceback_str = ''.join(traceback.format_tb(tb))
            message = f'{exc_type.__name__}: {exc_value}'
            Launch.finish_failed_item(self.name, message=message, reason=traceback_str)

def feature(name: str):
    def actual_decorator(cls):
        __tracebackhide__ = True

        original_setup = getattr(cls, 'setup_class', None)
        original_teardown = getattr(cls, 'teardown_class', None)
        item_id = Launch.create_report_item(
            name=name,
            type='suite',
            description=cls.__doc__)

        Launch.add_item(cls.__name__, item_id)
        Launch.add_item(name, item_id)

        @classmethod
        def new_teardown_class(cls, *args, **kwargs):
            if original_teardown is not None:
                original_teardown(*args, **kwargs)

            Launch.finish_item(cls.__name__)

        cls.teardown_class = new_teardown_class
        return cls

    return actual_decorator



def story(name: str):
    def actual_decorator(cls):
        original_setup = getattr(cls, 'setup_class', None)
        original_teardown = getattr(cls, 'teardown_class', None)
        parent = _get_class_parent(cls)
        item_id = Launch.create_report_item(
                name=name,
                parent_item=parent,
                type='story',
                description=cls.__doc__)

        Launch.add_item(cls.__name__, item_id)

        @classmethod
        def new_teardown_class(cls, *args, **kwargs):
            if original_teardown is not None:
                original_teardown(*args, **kwargs)

            Launch.finish_item(cls.__name__)

        cls.teardown_class = new_teardown_class

        return cls

    return actual_decorator


def log(*, message: str, level: str = "INFO"):
    __tracebackhide__ = True
    item = Launch.get_caller_name()
    Launch.create_log(item=item, message=message, level=level)

def attachment(*, name: str, attachment: Union[str, bytes], item: str = '', attachment_type: str, level: Literal["ERROR", "INFO", "DEBUG"] = "ERROR"):
    """Add attachment to the item (test class/case/step)
    :param item: The item name (function name)
    :param name: The attachment name
    :param attachment: attachment as bytes or the path to the attachment
    :param attachment_type: The type of the attachment (i.e use report.attachment_type.PNG)
    :param level: The log level of the the attachment (i.e if an error occured and you want to attach a screenshot use "ERROR")
    """
    Launch.add_attachment(item=item, message=name, level=level, attachment=attachment, attachment_type=attachment_type)