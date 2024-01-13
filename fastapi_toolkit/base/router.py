from abc import ABC, abstractmethod
from fastapi import APIRouter


class BaseRouter(APIRouter, ABC):
    snake_name: str
    snake_plural_name: str
    camel_name: str

    def __init__(self, config):
        super().__init__()
        self.prefix = f"/{self.snake_name}"
        self.tags = [self.camel_name]

        if config.get_one:
            self.add_api_route(
                path="/get_one",
                endpoint=self._get_one(),
                methods=["POST"],
                dependencies=config.get_one.guards,
                summary=f"Get one {self.snake_name}",
                description=f"Get one {self.snake_name}",
                response_description=f"A {self.snake_name}",
            )

        if config.get_all:
            self.add_api_route(
                path="/get_all",
                endpoint=self._get_all(),
                methods=["POST"],
                dependencies=config.get_all.guards,
                summary=f"Get all courses",
                description=f"Get all courses",
                response_description=f"All courses",
            )

        if config.get_link_all:
            self.add_api_route(
                path="/get_link_all",
                endpoint=self._get_link_all(),
                methods=["POST"],
                dependencies=config.get_link_all.guards,
                summary=f"Get all {self.snake_plural_name} with link",
                description=f"Get all {self.snake_plural_name} with link",
                response_description=f"All {self.snake_plural_name} with link",
            )

            if config.create_one:
                self.add_api_route(
                    path="/create_one",
                    endpoint=self._create_one(),
                    methods=["POST"],
                    dependencies=config.create_one.guards,
                    summary=f"Create one {self.snake_name}",
                    description=f"Create one {self.snake_name}",
                    response_description=f"Created {self.snake_name}",
                )

            if config.update_one:
                self.add_api_route(
                    path="/update_one",
                    endpoint=self._update_one(),
                    methods=["POST"],
                    dependencies=config.update_one.guards,
                    summary=f"Update one {self.snake_name}",
                    description=f"Update one {self.snake_name}",
                    response_description=f"Updated {self.snake_name}",
                )

            if config.delete_one:
                self.add_api_route(
                    path="/delete_one",
                    endpoint=self._delete_one(),
                    methods=["POST"],
                    dependencies=config.delete_one.guards,
                    summary=f"Delete one {self.snake_name}",
                    description=f"Delete one {self.snake_name}",
                    response_description=f"Deleted {self.snake_name}",
                )

    @abstractmethod
    def _get_one(self):
        raise NotImplementedError

    @abstractmethod
    def _get_all(self):
        raise NotImplementedError

    @abstractmethod
    def _get_link_all(self):
        raise NotImplementedError

    @abstractmethod
    def _create_one(self):
        raise NotImplementedError

    @abstractmethod
    def _update_one(self):
        raise NotImplementedError

    @abstractmethod
    def _delete_one(self):
        raise NotImplementedError
