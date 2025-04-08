import datetime as dt
import logging
import os
import re

import wpbot.bot_ui as bu
from wpbot.services.categories_service import CategoriesService
from wpbot.services.sources_service import SourcesService
from wpbot.services.users_service import UsersService
from telegram import Update
from telegram.ext import (ApplicationBuilder, CallbackContext,
                          CallbackQueryHandler, CommandHandler, MessageHandler,
                          filters)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_filename(in_filename: str):
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, in_filename)


def parse_time_text(message: str):
    result = []
    message_lines = message.strip().splitlines()

    for i in range(len(message_lines)):
        line = message_lines[i]
        match = re.match("^[0-9]+ [мч]$", line)
        if match is not None:
            number, unit = line.split()
            number = int(number)
            td = dt.timedelta(hours=number) if unit == "ч" else dt.timedelta(minutes=number)
            td = td.seconds
            result.append(td)
            continue
        elif line == "+" and i > 0:
            result.append(result[i - 1])
            continue
        try:
            line_split = line.split(", ")
            times = sorted([str(dt.datetime.strptime(time, "%H:%M").time()) for time in line_split])
            result.append(times)
        except Exception:
            raise RuntimeError("Failed to parse schedule")
    return result


class WPTelegramBot:
    def __init__(
        self,
        token: str,
        users_service: UsersService,
        categories_service: CategoriesService,
        sources_service: SourcesService,
    ):
        self.__categories_service = categories_service
        self.__users_service = users_service
        self.__sources_service = sources_service

        self.application = ApplicationBuilder().token(token).build()
        self.__setup_handlers()

    def __setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.__start))
        self.application.add_handler(CommandHandler("help", self.__help))
        self.application.add_handler(CommandHandler("setup", self.__setup))

        self.application.add_handler(CallbackQueryHandler(self.__button_handler))

        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.__message_handler_schedule)
        )

        self.application.add_error_handler(self.__error_handler)

    async def __start(self, update: Update, context: CallbackContext) -> None:
        user_id = update.message.from_user.id
        if self.__users_service.get_user(user_id) is None:
            self.__users_service.insert_user(user_id)

        with open(get_filename("prompts/greeting.txt")) as f:
            await update.message.reply_text(f.read())

    async def __help(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("Here's how I can help you...")

    async def __setup(self, update: Update, context: CallbackContext) -> None:
        if update.message is not None:
            user_id = update.message.from_user.id
        else:
            user_id = update.callback_query.from_user.id
        await bu.show_setup_menu(
            update, context, all(self.__users_service.is_setup_finished(user_id))
        )

    async def __setup_schedule(
        self, update: Update, context: CallbackContext, subcommand: str, user_id: int
    ):
        if subcommand == "time":
            with open(get_filename("prompts/time_input.txt")) as f:
                await update.callback_query.message.reply_text(f.read())

        if subcommand.count("=") == 1:
            param, value = subcommand.split("=")
            if param == "days":
                self.__users_service.update_user_schedule(
                    user_id, "everyday" if value == "everyday" else {value: []}
                )

        schedule_items = self.__users_service.get_user_settings(user_id)["schedule"].items()
        has_days_selected = any(filter(lambda x: x[-1] is not None, schedule_items))
        await bu.show_schedule_menu(update, context, has_days_selected, schedule_items)

    async def __setup_categories(
        self, update: Update, context: CallbackContext, subcommand: str, user_id: int
    ):
        user_categories = self.__categories_service.get_for_user(user_id)
        all_categories = self.__categories_service.get_all()

        if subcommand.count("=") == 1:
            param, value = subcommand.split("=")
            if param == "cat":
                category_index, is_user_category = value.split(" ")
                category = all_categories[int(category_index)]
                matched_user_category = next(
                    filter(lambda x: x["_id"] == category["_id"], user_categories)
                )
                if matched_user_category is not None:
                    await bu.show_category_setup_menu(
                        update,
                        context,
                        is_user_category == "True",
                        int(category_index),
                        matched_user_category,
                    )
                else:
                    await bu.show_category_setup_menu(
                        update, context, is_user_category == "True", int(category_index), category
                    )
                return
            elif param == "score":
                category_index = int(value)
                await bu.show_score_keyboard(update, context, category_index)
                return
            elif param == "score_apply":
                index, score = list(map(int, value.split(" ")))
                self.__users_service.update_user_category_score(
                    user_id, all_categories[index]["_id"], score
                )
                await bu.show_category_setup_menu(
                    update, context, True, index, {"score": score, **all_categories[index]}
                )
                return
            elif param == "add":
                index = int(value)
                new_category = {
                    "id": all_categories[index]["_id"],
                    "score": None,
                }
                self.__users_service.add_user_category(user_id, new_category)
                await bu.show_score_keyboard(update, context, index)
                return
            elif param == "del":
                index = int(value)
                self.__users_service.remove_user_category(user_id, all_categories[index]["_id"])
                await bu.show_category_setup_menu(
                    update, context, False, index, all_categories[index]
                )
                return
        elif subcommand == "finish":
            await self.__setup(update, context)
            return

        is_setup_finished = len(user_categories) > 0 and any(
            filter(lambda x: x["score"] is not None, user_categories)
        )
        await bu.show_categories_setup_menu(
            update, context, is_setup_finished, all_categories, user_categories
        )

    async def __setup_sources(
        self, update: Update, context: CallbackContext, subcommand: str, user_id: int
    ):
        user_sources: list = self.__users_service.get_user_settings(user_id)["sources"]
        all_sources = self.__sources_service.get_all()

        if subcommand.count("=") == 1:
            param, value = subcommand.split("=")
            if param == "src":
                index, is_used_source = value.split()
                src_id = all_sources[int(index)]["_id"]
                if is_used_source == "False":
                    self.__users_service.add_used_source(user_id, src_id)
                    user_sources.append(src_id)
                else:
                    self.__users_service.remove_used_source(user_id, src_id)
                    user_sources.remove(src_id)
        elif subcommand == "finish":
            await self.__setup(update, context)
            return

        is_setup_finished = len(user_sources) > 0
        await bu.show_sources_setup_menu(
            update, context, is_setup_finished, all_sources, user_sources
        )

    async def __button_handler(self, update: Update, context: CallbackContext):
        user_id = update.callback_query.from_user.id
        query = update.callback_query
        await query.answer()

        command, subcommand = query.data.split(":")
        if command == "sch":
            await self.__setup_schedule(update, context, subcommand, user_id)
        elif command == "cat":
            await self.__setup_categories(update, context, subcommand, user_id)
        elif command == "src":
            await self.__setup_sources(update, context, subcommand, user_id)

    async def __message_handler_schedule(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        user_schedule = self.__users_service.get_user_settings(user_id)["schedule"]
        schedule_times = parse_time_text(update.message.text)
        if len(schedule_times) == 1:
            user_schedule = {
                k: (schedule_times[0] if v is not None else None) for k, v in user_schedule.items()
            }
        else:
            old_schedule = user_schedule.copy()
            i = 0
            keys = user_schedule.keys()
            for k in keys:
                if user_schedule[k] is None:
                    continue
                if i >= len(schedule_times):
                    user_schedule = old_schedule
                    raise RuntimeError()
                user_schedule[k] = schedule_times[i]
                i += 1
        self.__users_service.update_user_schedule(user_id, user_schedule)
        await update.message.reply_text("Настройки сохранены!")
        await self.__setup(update, context)

    async def __error_handler(self, update: Update, context: CallbackContext):
        logging.error(msg="An exception occurred", exc_info=context.error)
        if isinstance(update, Update) and update.message:
            await update.message.reply_text("Произошла ошибка!")

    async def run(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

