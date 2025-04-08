import os

from wpbot.bot import WPTelegramBot
from wpbot.database.categories_repository import CategoriesRepository
from wpbot.database.mongo_context import MongoDBConnectionManager
from wpbot.database.sources_repository import SourcesRepository
from wpbot.database.users_repository import UsersRepository
from dependency_injector import containers, providers
from wpbot.services.categories_service import CategoriesService
from wpbot.services.sources_service import SourcesService
from wpbot.services.users_service import UsersService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_dict(
        {
            "TG_TOKEN": os.getenv("TG_TOKEN"),
            "MONGO_PASSWORD": os.getenv("MONGO_PASSWORD"),
            "MONGO_HOST": os.getenv("MONGO_HOST")
        }
    )

    manager = providers.Singleton(MongoDBConnectionManager, config.MONGO_PASSWORD, config.MONGO_HOST)

    users_repository = providers.Factory(UsersRepository, manager)
    categories_repository = providers.Factory(CategoriesRepository, manager)
    sources_repository = providers.Factory(SourcesRepository, manager)

    users_service = providers.Factory(UsersService, users_repository)
    categories_service = providers.Factory(CategoriesService, categories_repository)
    sources_service = providers.Factory(SourcesService, sources_repository)

    bot = providers.Factory(
        WPTelegramBot, config.TG_TOKEN, users_service, categories_service, sources_service
    )


async def main():
    container = Container()
    bot = container.bot()
    await bot.run()


if __name__ == "__main__":
    main()
