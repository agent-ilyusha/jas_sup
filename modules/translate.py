# -- coding: utf-8
from transformers import pipeline


def translate_txt(txt: str, flag: bool) -> str:
    """
    Translates text to English language and vice versa.
    :param txt: Text to translate.
    :param flag: Flag to choice model.
    :return: 
    """
    if flag:
        translator = pipeline("translation_RU_to_EN", model="Helsinki-NLP/opus-mt-ru-en")
    else:
        translator = pipeline("translation_EN_to_RU", model="Helsinki-NLP/opus-mt-en-ru")
    translated_text = translator(txt)
    return translated_text


if __name__ == "__main__":
    print(translate_txt("Скачанная музыка", True))
