from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext


async def show_schedule_menu(
    update: Update, context: CallbackContext, has_days_selected: bool, schedule_items: dict
):
    command_prefix = "setup_schedule"
    keyboard = [
        [
            InlineKeyboardButton(
                f"{option}{' ✅' if times is not None else ''}",
                callback_data=f"{command_prefix}:days={option}",
            )
            for option, times in schedule_items
        ],
        [
            InlineKeyboardButton(
                "Ежедневно",
                callback_data=f"{command_prefix}:days=everyday",
            )
        ],
    ]
    if has_days_selected:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "Установить время рассылки",
                    callback_data=f"{command_prefix}:time",
                )
            ]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        "Выберите дни, в которые будет производиться рассылка", reply_markup=reply_markup
    )


async def show_setup_menu(update: Update, context: CallbackContext, is_setup_finished: bool):
    keyboard = [
        [InlineKeyboardButton("Настроить расписание", callback_data="sch:")],
        [InlineKeyboardButton("Настроить категории новостей", callback_data="cat:")],
        [InlineKeyboardButton("Настроить источники", callback_data="src:")],
    ]
    if is_setup_finished:
        keyboard.append([InlineKeyboardButton("Завершить настройку", callback_data="setup_finish")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message is not None:
        await update.message.reply_text("Выберите действие", reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(
            "Выберите действие", reply_markup=reply_markup
        )


def print_categories_info(all_categories: list[dict], user_categories: list[dict]) -> str:
    current_topic = ""
    result = "Выбранные категории\n"
    for cat in user_categories:
        if cat["topic"] != current_topic:
            current_topic = cat["topic"]
            result += current_topic + ":\n"
        score_value = cat["score"] if cat["score"] is not None else "Н/У"
        result += f"- {cat["name"]} {score_value}\n"

    user_categories_ids = [cat["_id"] for cat in user_categories]
    other_categories = list(filter(lambda x: x["_id"] not in user_categories_ids, all_categories))

    current_topic = ""
    result += "\n\nДоступные категории\n"
    for cat in other_categories:
        if cat["topic"] != current_topic:
            current_topic = cat["topic"]
            result += current_topic + "\n"
        result += f"- {cat["name"]}\n"
    return result


async def show_categories_setup_menu(
    update: Update,
    context: CallbackContext,
    is_setup_finished: bool,
    all_categories: list[dict],
    user_categories: list[dict],
):
    user_categories_ids = [cat["_id"] for cat in user_categories]
    keyboard = [
        [
            InlineKeyboardButton(
                category["name"] + (" ✅" if category["_id"] in user_categories_ids else ""),
                callback_data=f"cat:cat={i} {category["_id"] in user_categories_ids}",
            )
        ]
        for i, category in enumerate(all_categories)
    ]
    if is_setup_finished:
        keyboard.append([InlineKeyboardButton("⬅️ Завершить настройку", callback_data="cat:finish")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        print_categories_info(all_categories, user_categories), reply_markup=reply_markup
    )


def print_category_info(category: dict):
    result = f"Выбранная категория \"{category['name']}\""
    if "score" in category.keys():
        result += f"\nОценка {category['score']}"
    return result


async def show_category_setup_menu(
    update: Update,
    context: CallbackContext,
    is_user_category: bool,
    category_index: int,
    category: dict[str],
):
    if is_user_category:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Изменить оценку", callback_data=f"cat:score={category_index}"
                ),
                InlineKeyboardButton("Удалить", callback_data=f"cat:del={category_index}"),
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton("Добавить", callback_data=f"cat:add={category_index}"),
            ]
        ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="cat:back")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        print_category_info(category), reply_markup=reply_markup
    )


async def show_score_keyboard(update: Update, context: CallbackContext, category_index: int):
    keys = [
        InlineKeyboardButton(str(i), callback_data=f"cat:score_apply={category_index} {i}")
        for i in range(1, 11)
    ]
    keyboard = [keys[:5], keys[5:]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text("Введите оценку", reply_markup=reply_markup)


async def show_sources_setup_menu(
    update: Update,
    context: CallbackContext,
    is_setup_finished: bool,
    all_sources: list[dict],
    user_sources_ids: list[dict],
):
    keyboard = [
        [
            InlineKeyboardButton(
                src["name"] + (" ✅" if src["_id"] in user_sources_ids else ""),
                callback_data=f"src:src={i} {src["_id"] in user_sources_ids}",
            )
        ]
        for i, src in enumerate(all_sources)
    ]
    if is_setup_finished:
        keyboard.append([InlineKeyboardButton("⬅️ Завершить настройку", callback_data="src:finish")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text("Выберите источники", reply_markup=reply_markup)
