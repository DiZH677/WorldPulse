from wpbot.database.mongo_context import MongoDBConnectionManager


class CategoriesRepositoryError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class CategoriesRepository:
    def __init__(self, manager: MongoDBConnectionManager):
        self.__db = manager.db

    def get_all_categories(self):
        return self.__db.categories.find().sort("topic").to_list()

    def get_user_categories(self, user_id: int):
        return self.__db.users.aggregate(
            [
                {"$match": {"_id": user_id}},
                {"$unwind": "$settings.categories"},
                {"$addFields": {"category_id": {"$toObjectId": "$settings.categories.id"}}},
                {
                    "$lookup": {
                        "from": "categories",
                        "localField": "category_id",
                        "foreignField": "_id",
                        "as": "categoryDetails",
                    }
                },
                {"$unwind": "$categoryDetails"},
                {
                    "$project": {
                        "_id": "$settings.categories.id",
                        "score": "$settings.categories.score",
                        "name": "$categoryDetails.name",
                        "topic": "$categoryDetails.topic",
                    }
                },
                {"$sort": {"topic": 1}},
            ]
        ).to_list()
