from wpbot.database.sources_repository import SourcesRepository


class SourcesService:
    def __init__(self, sources_repository: SourcesRepository):
        self.__sources_repository = sources_repository

    def get_all(self) -> dict | None:
        return self.__sources_repository.get_all()
