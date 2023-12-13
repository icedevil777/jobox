from . import models


def dict_key_parser(get_dict: dict, start_text):
    employment_types = []
    _startswith_text = start_text
    for key in list(get_dict.keys()):
        if key.startswith(_startswith_text):
            employment_types.append(
                key.replace(_startswith_text, '')
            )

    return employment_types


def translate(text: str):

    russian = ['ё', 'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х',
               'ъ', 'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э',
               '\\', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '.', 'Ё',
               'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ',
               'Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', '/',
               'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', ',']
    english = ['§', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[',
               ']', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'',
               '\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '±',
               'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}',
               'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', '|',
               'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?']
    for i, x in enumerate(english):
        text = text.replace(x, russian[i])
    return text

