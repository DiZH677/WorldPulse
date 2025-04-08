from wpbot.database.mongo_context import MongoDBConnectionManager


class UsersRepositoryError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class UsersRepository:
    def __init__(self, manager: MongoDBConnectionManager):
        self.__db = manager.db

    def get_user(self, user_id: int) -> dict | None:
        return self.__db.users.find_one({"_id": user_id})

    def insert_user(self, user_id: int, user_settings: dict):
        self.__db.users.insert_one(document={"_id": user_id, "settings": user_settings})

    def update_user_schedule(self, user_id: int, user_schedule: dict):
        self.__db.users.update_one(
            filter={"_id": user_id}, update={"$set": {"settings.schedule": user_schedule}}
        )

    def add_user_category(self, user_id: int, user_category: dict):
        self.__db.users.update_one(
            filter={"_id": user_id}, update={"$push": {"settings.categories": user_category}}
        )

    def update_user_category_score(self, user_id: int, category_id: str, score: int):
        self.__db.users.update_one(
            {"_id": user_id, "settings.categories": {"$elemMatch": {"id": category_id}}},
            {"$set": {"settings.categories.$.score": score}},
        )

    def remove_user_category(self, user_id: int, category_id: str):
        self.__db.users.update_one(
            filter={"_id": user_id}, update={"$pull": {"settings.categories": {"id": category_id}}}
        )

    def add_used_source(self, user_id: int, source_id: str):
        self.__db.users.update_one(
            filter={"_id": user_id}, update={"$push": {"settings.sources": source_id}}
        )

    def remove_used_source(self, user_id: int, source_id: str):
        self.__db.users.update_one(
            filter={"_id": user_id}, update={"$pull": {"settings.sources": source_id}}
        )
