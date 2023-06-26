import inspect
import asyncio
import json
from ._internal import Launch


__all__ = ['_run_func', '_get_class_parent', '_is_fixture']

def _run_func(func, *args, **kwargs):
    __tracebackhide__ = True
    if inspect.iscoroutinefunction(func):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError as e:
            if "no running event loop" in str(e):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            else:
                raise e

            return loop.run_until_complete(func(*args, **kwargs))

    return func(*args, **kwargs)


def _get_class_parent(child_class):
    __tracebackhide__ = True
    for base_class in child_class.__bases__:
        base_class_name = base_class.__name__
        
        if base_class_name in Launch.items().keys():
            return base_class_name
        
        elif len(base_class.__bases__) > 0 :
            result = _get_class_parent(base_class)
            
            if result:
                return result

    return None

def _is_fixture(func, *args, **kwargs):
    return True if 'request' in kwargs.keys() else False

