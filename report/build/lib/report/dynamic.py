from ._internal import Launch
from typing import Optional
class dynamic:
    @staticmethod
    def step(name: str, parent: Optional[str] = None):
        try:
            caller = Launch.get_caller_name() if not parent else parent
            item_id = Launch.create_report_item(
                        name=name,
                        parent_item=caller,
                        type='step',
                        description='')

            Launch.items[caller] = item_id
        finally:
            print(f'finish {caller}')
            Launch.finish_item(caller)

    @staticmethod
    def title(test_title: str):
        try:
            caller = Launch.get_caller_name()
            item_id = Launch.create_report_item(
                        name=test_title,
                        parent_item=caller,
                        type='test',
                        description='')

            Launch.items[caller] = item_id

        finally:
            Launch.finish_item(caller)