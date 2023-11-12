alphabet_equalisation_map = {'آ': 'ا', 'إ': 'ا', 'أ': 'ا', 'ؤ': 'و', 'ئ': 'ی', 'ة': 'ه',
                             'ä': 'a', 'ö': 'o', 'ü': 'u', 'ë': 'e', 'ï': 'i', 'ÿ': 'y', 'œ': 'oe', 'æ': 'ae'
                             }

sorting_translation_map = {
    'ا': '1', 'ب': '2', 'پ': '3', 'ت': '4', 'ث': '5', 'ج': '6', 'چ': '7', 'ح': '8',
    'خ': 'a', 'د': 'b',
    'ذ': 'c', 'ر': 'd',
    'ز': 'e', 'ژ': 'f', 'س': 'g', 'ش': 'h', 'ص': 'i', 'ض': 'j', 'ط': 'k', 'ظ': 'l', 'ع': 'm', 'غ': 'n', 'ف': 'o',
    'ق': 'p', 'ک': 'q', 'گ': 'r', 'ل': 's', 'م': 't', 'ن': 'u', 'و': 'v', 'ؤ': 'v', 'ه': 'w', 'ی': 'x',
}

short_vowels = ['']


def translate_to_sorting_value(value):
    return ''.join([sorting_translation_map.get(x) if sorting_translation_map.get(x) else x for x in value])


def remove_short_vowels_(value):
    return ''.join([x if x not in ['ْ', 'ٌ', 'ٍ', 'ً', 'ُ', 'ِ', 'َ', 'ّ', 'ٓ', 'ٔ'] else '' for x in value])


def remove_spaces(value):
    value = value.replace(' ', '')
    value = value.replace('\u200c', '')
    value = value.replace('\u200b', '')
    return value


def remove_short_vowels(value):
    return ''.join([x if x not in ['ْ', 'ٌ', 'ٍ', 'ً', 'ُ', 'ِ', 'َ', 'ّ', 'ٓ', 'ٔ'] else '' for x in value])


def equalize_alphabets(value):
    for k, v in alphabet_equalisation_map.items():
        value = value.replace(k, v)
    return value


def clean_value(value):
    value = remove_spaces(value)
    value = remove_short_vowels(value)
    value = equalize_alphabets(value)
    return value
