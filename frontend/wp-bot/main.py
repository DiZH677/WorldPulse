import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application, CallbackContext, CallbackQueryHandler,
                          CommandHandler, MessageHandler, filters)
from user_settings_builder import (ScheduleSetupStage, SetupStage,
                                   UserSettingsBuilder)

TIME_TEMPLATE = """Введите время, в которое будет производиться рассылка.

Допустимые форматы: ЧЧ:ММ, "каждые N м/ч"

Чтобы установить расписание, перечислите нужное время в формате ЧЧ:ММ через запятую на одной строке.
Для одного дня -- одна строка.
Строка с символом "+" означает повтор расписания, установленного для предыдущего дня.

Если выбрано несколько дней, но введена одна строка с расписанием, то оно будет применено для всех \
выбранных дней.
"""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


settings_builder = UserSettingsBuilder()


async def setup(update):
    global settings_builder

    keyboard = [
        [InlineKeyboardButton("Настроить расписание", callback_data=SetupStage.Schedule)],
        [InlineKeyboardButton("Настроить категории новостей", callback_data=SetupStage.Categories)],
        [InlineKeyboardButton("Настроить категории новостей", callback_data=SetupStage.Sources)],
    ]

    if settings_builder.is_setup_finished():
        keyboard.append(
            [InlineKeyboardButton("Завершить настройку", callback_data=SetupStage.Finished)]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message is not None:
        await update.message.reply_text("Выберите действие", reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text(
            "Выберите действие", reply_markup=reply_markup
        )


async def schedule_days(update, context):
    global settings_builder

    keyboard = [
        [
            InlineKeyboardButton(
                f"{option}{' ✅' if times is not None else ''}", callback_data=option
            )
            for option, times in settings_builder.schedule.items()
        ],
        [
            InlineKeyboardButton(
                "Ежедневно",
                callback_data="Ежедневно",
            )
        ],
    ]
    if settings_builder.is_schedule_setup_finished():
        keyboard.append(
            [
                InlineKeyboardButton(
                    "Установить время рассылки",
                    callback_data=ScheduleSetupStage.Time,
                )
            ]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        "Выберите дни, в которые будет производиться рассылка", reply_markup=reply_markup
    )


async def schedule_time(update, context):
    await update.callback_query.message.reply_text(TIME_TEMPLATE)


async def start(update, context):
    await setup(update)


async def button_handler(update: Update, context: CallbackContext):
    global settings_builder

    query = update.callback_query
    await query.answer()
    if query.data == SetupStage.Schedule:
        await schedule_days(update, context)
    elif query.data in settings_builder.schedule or query.data == "Ежедневно":
        settings_builder.update_schedule_days(query.data)
        await schedule_days(update, context)
    elif query.data == ScheduleSetupStage.Time:
        await schedule_time(update, context)
    elif query.data == SetupStage.Categories:
        await query.edit_message_text(text="Doing categories")
    elif query.data == SetupStage.Sources:
        await query.edit_message_text(text="Doing sources")
    elif query.data == "Завершить":
        await setup(update)


async def message_handler_time(update: Update, context: CallbackContext):
    global settings_builder

    user_message = update.message.text
    settings_builder.update_schedule_time(user_message)
    logging.info(settings_builder.schedule)


async def error_handler(update: Update, context: CallbackContext):
    logging.error(msg="An exception occurred", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("Oops, something went wrong!")


def main():
    application = Application.builder().token(os.getenv("TG_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler_time))
    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
