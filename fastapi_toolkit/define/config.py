from typing import Union, List

from fastapi import Security


class RouteConfig:
    guards: List[Security] = []

    def __init__(self, guards: List[Security] = None):
        if guards is not None:
            self.guards = guards


class ModelConfig:
    get_one: Union[RouteConfig, bool] = RouteConfig()
    get_link_one: Union[RouteConfig, bool] = RouteConfig()
    get_all: Union[RouteConfig, bool] = RouteConfig()
    get_link_all: Union[RouteConfig, bool] = RouteConfig()
    create_one: Union[RouteConfig, bool] = RouteConfig()
    update_one: Union[RouteConfig, bool] = RouteConfig()
    delete_one: Union[RouteConfig, bool] = RouteConfig()
