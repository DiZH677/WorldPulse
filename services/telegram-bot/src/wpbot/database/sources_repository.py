from wpbot.database.mongo_context import MongoDBConnectionManager


class SourcesRepositoryError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class SourcesRepository:
    def __init__(self, manager: MongoDBConnectionManager):
        self.__db = manager.db

    def get_all(self) -> dict | None:
        return self.__db.sources.find().sort("name").to_list()
