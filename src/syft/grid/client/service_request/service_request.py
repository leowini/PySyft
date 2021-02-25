# stdlib
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

# third party
from pandas import DataFrame

# syft relative
from ....core.common.message import SyftMessage


class GridServiceRequest:
    def __init__(
        self,
        create_msg,
        get_msg,
        get_all_msg,
        update_msg,
        delete_msg,
        send,
        response_key=None,
    ):
        self.__create_message = create_msg
        self.__get_message = get_msg
        self.__get_all_message = get_all_msg
        self.__update_message = update_msg
        self.__delete_message = delete_msg
        self.__send = send
        self.__response_key = response_key

    def create(self, **kwargs):
        return self.__send(grid_msg=self.__create_message, content=kwargs)

    def get(self, **kwargs):
        return self.to_obj(self.__send(grid_msg=self.__get_message, content=kwargs))

    def all(self, pandas: bool = False):
        result = self.__send(grid_msg=self.__get_all_message)
        if pandas:
            return self.to_dataframe(result)
        else:
            return result

    def update(self, **kwargs):
        return self.__send(grid_msg=self.__update_message, content=kwargs)

    def delete(self, **kwargs):
        return self.__send(grid_msg=self.__delete_message, content=kwargs)

    def to_dataframe(self, result: Dict[Any, Any]):
        return DataFrame(result.get(self.__response_key + "s", []))

    def to_obj(self, result: Dict[Any, Any]):
        _user = result.get(self.__response_key, None)

        if _user:
            _class_name = self.__response_key.capitalize()
            _user = type(_class_name, (object,), _user)()

        return _user
