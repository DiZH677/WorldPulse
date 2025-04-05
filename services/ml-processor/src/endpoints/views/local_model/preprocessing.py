import re


def remove_emojis(text):
    # Регулярное выражение для поиска эмодзи
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # Смайлы лиц
        u"\U0001F300-\U0001F5FF"  # Символы и геометрические формы
        u"\U0001F680-\U0001F6FF"  # Транспорт и карты
        u"\U0001F700-\U0001F77F"  # Алхимия
        u"\U0001F780-\U0001F7FF"  # Геометрические фигуры
        u"\U0001F800-\U0001F8FF"  # Постоянные изображения
        u"\U0001F900-\U0001F9FF"  # Разнообразие смайлов
        u"\U0001FA00-\U0001FAFF"  # Символы для дополнительной информации
        u"\U00002700-\U000027BF"  # Разные символы
        u"\U0001F1E0-\U0001F1FF"  # Флаги стран
        u"\U00002600-\U000026FF"  # Символы погоды, включая молнию
        u"\U000027A0-\U000027BF"  # Дополнительно вспомогательные символы
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def trim_spaces(text):
    trimmed_text = ' '.join(text.split()).strip()
    return trimmed_text

def trim_spec_symbols(text):
    trimmed_text = text
    for i in range(10):
        for s in "=|\/+#@":
            trimmed_text = trimmed_text.replace(s, "")
        trimmed_text = trimmed_text.replace("--", "")
    return trimmed_text

def full_preprocessing(text):
    return trim_spec_symbols(trim_spaces(remove_emojis(text)))
