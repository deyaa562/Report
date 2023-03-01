from ._internal import Launch
import inspect

async def _run_func(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)

    return func(*args, **kwargs)

def step(name: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            parent = Launch.get_caller_name()
            item_id = Launch.create_report_item(
                name=name,
                parent_item=parent,
                type='step',
                has_stats=False,
                description=func.__doc__)

            Launch.items[func.__name__] = item_id
            result = None
            try:
                result = await _run_func(func, *args, **kwargs)

            except Exception as exception:
                Launch.finish_failed_item(func.__name__, str(exception))
                raise exception

            Launch.finish_passed_item(func.__name__)
            return result

        return wrapper
    return decorator

def title(name: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            item_id = Launch.create_report_item(
                name=name,
                parent_item=Launch.get_enclosing_class_name(func),
                type='test',
                description=func.__doc__)

            Launch.items[func.__name__] = item_id
            result = await _run_func(func, *args, **kwargs)
            Launch.finish_item(func.__name__)
            return result

        return wrapper
    return decorator

def feature(name: str):
    def decorator(cls):
        item_id = Launch.create_report_item(
            name=name,
            type='suite',
            description=cls.__doc__)

        Launch.items[cls.__name__] = item_id
        return cls

    return decorator

def story(name: str):
    def decorator(cls):

        parent = cls.__mro__[1].__name__
        item_id = Launch.create_report_item(
            name=name,
            parent_item=parent,
            type='story',
            description=cls.__doc__)

        Launch.items[cls.__name__] = item_id
        return cls

    return decorator


