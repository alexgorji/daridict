sorting_translation_map = {
    'آ': '1', 'ا': '2', 'ب': '3', 'پ': '4', 'ت': '5', 'ث': '6', 'ج': '7', 'چ': '8', 'ح': '9', 'خ': 'a', 'د': 'b',
    'ذ': 'c', 'ر': 'd',
    'ز': 'e', 'ژ': 'f', 'س': 'g', 'ش': 'h', 'ص': 'i', 'ض': 'j', 'ط': 'k', 'ظ': 'l', 'ع': 'm', 'غ': 'n', 'ف': 'o',
    'ق': 'p', 'ک': 'q', 'گ': 'r', 'ل': 's', 'م': 't', 'ن': 'u', 'و': 'v', 'ؤ': 'v', 'ه': 'w', 'ۀ': 'w', 'ی': 'x',
    'ئ': 'x',
    'ä': 'a', 'ö': 'o', 'ü': 'u',
}

persian_letters = ['آ', 'ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط',
                   'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی']


def translate_to_sorting_value(value):
    return ''.join([sorting_translation_map.get(x) if sorting_translation_map.get(x) else x for x in value])


def remove_short_vowels(value):
    return ''.join([x if x not in ['َ', 'ِ', 'ُ'] else '' for x in value])


def remove_redundant_spaces(value):
    value = value.strip()
    value = value.strip('\u200c')
    value = value.strip('\u200b')
    return value


def equalize_alef(value):
    return value.replace('آ', 'ا')
