from .models import DictItem, DictEntry, DictLanguage, DictNode


def delete_not_noded_items():
    for item in DictItem.objects.all():
        if not item.dictnode_set.all() and not (item.item_dari.all() or item.item_farsi.all() or item.item_german.all()):
            item.delete()

def check_items():
    for item in DictItem.objects.all():
        if not item.dictnode_set.all() and (item.item_dari.all() or item.item_farsi.all() or item.item_german.all()):
            print(f'item {item} no node but entry')
        if item.dictnode_set.all() and not (item.item_dari.all() or item.item_farsi.all() or item.item_german.all()):
            print(f'item {item} no entry but node')

def delete_all_entries():
    for entry in DictEntry.objects.all():
        entry.delete()


def create_entries(item_dari, item_farsi, item_german):
    dari = DictLanguage.objects.get_or_create(value='Dari')[0]
    farsi = DictLanguage.objects.get_or_create(value='Farsi')[0]
    german = DictLanguage.objects.get_or_create(value='Deutsch')[0]

    def create_item(item, language):
        item = DictItem.objects.get(id=item.id)
        if not item:
            item = DictItem.objects.create(value=item.value, language=language)
        return item

    if item_dari:
        item_dari = create_item(item_dari, dari)

    if item_farsi:
        item_farsi = create_item(item_farsi, farsi)

    if item_german:
        item_german = create_item(item_german, german)

    return DictEntry.objects.get_or_create(item_dari=item_dari, item_farsi=item_farsi, item_german=item_german)[0]


def translate_dict_node_to_dict_entries():
    for node in DictNode.objects.all():
        item_dari = None
        item_farsi = None
        item_german = None
        for item in node.items.all():
            if item.language.value == 'Dari':
                item_dari = item
            elif item.language.value == 'Farsi':
                item_farsi = item
            else:
                item_german = item
        # print(node.id, item_dari, item_farsi, item_german)
        create_entries(item_dari, item_farsi, item_german)


def remove_short_vowels(value):
    return ''.join([x if x not in ['َ', 'ِ', 'ُ'] else '' for x in value])


def remove_redundant_spaces(value):
    value = value.strip()
    value = value.strip('\u200c')
    value = value.strip('\u200b')
    return value


def fill_cleaned_values():
    for dict_item in DictItem.objects.all():
        dict_item.cleaned_value = remove_redundant_spaces(dict_item.value)
        if dict_item.language.value in ['Dari', 'Farsi']:
            dict_item.cleaned_value = remove_short_vowels(dict_item.cleaned_value)

        dict_item.save()


sorting_translation_map = {
    'آ': '1', 'ا': '2', 'ب': '3', 'پ': '4', 'ت': '5', 'ث': '6', 'ج': '7', 'چ': '8', 'ح': '9', 'خ': 'a', 'د': 'b',
    'ذ': 'c', 'ر': 'd',
    'ز': 'e', 'ژ': 'f', 'س': 'g', 'ش': 'h', 'ص': 'i', 'ض': 'j', 'ط': 'k', 'ظ': 'l', 'ع': 'm', 'غ': 'n', 'ف': 'o',
    'ق': 'p', 'ک': 'q', 'گ': 'r', 'ل': 's', 'م': 't', 'ن': 'u', 'و': 'v',
    'ه': 'w', 'ی': 'x'
}


def translate_to_sorting_value(value):
    return ''.join([sorting_translation_map.get(x) if sorting_translation_map.get(x) else x for x in value])


def fill_sorting_values():
    for dict_item in DictItem.objects.all():
        if dict_item.language.value in ['Dari', 'Farsi']:
            dict_item.sorting_value = translate_to_sorting_value(dict_item.cleaned_value)
        else:
            dict_item.sorting_value = dict_item.cleaned_value

        dict_item.save()

def remove_empty_items():
    for entry in DictEntry.objects.all():
        print(entry)
        save = False
        if entry.item_dari and entry.item_dari.value == '':
            entry.item_dari = None
            save = True
        if entry.item_farsi and entry.item_farsi.value == '':
            entry.item_farsi = None
            save = True
        if entry.item_german and entry.item_german.value == '':
            entry.item_german = None
            save = True
        if save:
            entry.save()
