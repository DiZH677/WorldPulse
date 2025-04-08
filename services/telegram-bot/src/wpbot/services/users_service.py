from wpbot.database.users_repository import UsersRepository

EMPTY_SCHEDULE = {
    "Пн": None,
    "Вт": None,
    "Ср": None,
    "Чт": None,
    "Пт": None,
    "Сб": None,
    "Вс": None,
}


class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.__users_repository = users_repository

    def get_user(self, user_id: int) -> dict | None:
        return self.__users_repository.get_user(user_id)

    def insert_user(self, user_id: int):
        self.__users_repository.insert_user(
            user_id, {"schedule": EMPTY_SCHEDULE, "categories": [], "sources": []}
        )

    def get_user_settings(self, user_id: int) -> dict | None:
        user = self.__users_repository.get_user(user_id)
        return user["settings"] if user is not None else None

    def update_user_schedule(self, user_id: int, schedule: dict | str):
        user_schedule = self.get_user_settings(user_id)["schedule"]
        if isinstance(schedule, str):
            value = (
                None
                if len(list(filter(lambda x: x is not None, user_schedule.values()))) > 0
                else []
            )
            user_schedule = {key: value for key, _ in user_schedule.items()}
        else:
            for k, v in schedule.items():
                user_schedule[k] = v if user_schedule[k] is not None else None
        self.__users_repository.update_user_schedule(user_id, user_schedule)

    def add_user_category(self, user_id: int, category: dict):
        self.__users_repository.add_user_category(user_id, category)

    def update_user_category_score(self, user_id: int, category_id: str, score: int):
        self.__users_repository.update_user_category_score(user_id, category_id, score)

    def remove_user_category(self, user_id: int, category_id: str):
        self.__users_repository.remove_user_category(user_id, category_id)

    def add_used_source(self, user_id: int, source_id: str):
        self.__users_repository.add_used_source(user_id, source_id)

    def remove_used_source(self, user_id: int, source_id: str):
        self.__users_repository.remove_used_source(user_id, source_id)

    def is_setup_finished(self, user_id: int) -> tuple[bool, bool, bool]:
        settings = self.get_user_settings(user_id)
        if settings is None:
            return False

        schedule = any(settings["schedule"].values())
        categories = any(settings["categories"])
        sources = any(settings["sources"])

        return (schedule, categories, sources)
