from wpbot.database.categories_repository import CategoriesRepository


class CategoriesService:
    def __init__(self, categories_repository: CategoriesRepository):
        self.__categories_repository = categories_repository

    def get_all(self) -> list:
        return self.__categories_repository.get_all_categories()

    def get_for_user(self, user_id: int) -> list:
        categories = self.__categories_repository.get_user_categories(user_id)
        return categories
