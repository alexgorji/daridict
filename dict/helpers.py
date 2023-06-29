from .models import DictItem, DictEntry, DictLanguage, DictNode


def create_entries(item_dari, item_farsi, item_german):
    # create dictionary entries
    dari = DictLanguage.objects.get_or_create(value='Dari')[0]
    farsi = DictLanguage.objects.get_or_create(value='Farsi')[0]
    german = DictLanguage.objects.get_or_create(value='German')[0]

    def create_item(item, language):
        return DictItem.objects.get_or_create(value=item, language=language)[0]

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
        print(node.id, item_dari, item_farsi, item_german)
        create_entries(item_dari, item_farsi, item_german)


def remove_short_vowels(value):
    return ''.join([x if x not in ['َ', 'ِ', 'ُ'] else '' for x in value])


def fill_cleaned_values():
    for dict_item in DictItem.objects.all():
        if dict_item.language.value in ['Dari', 'Farsi']:
            dict_item.cleaned_value = remove_short_vowels(dict_item.value)
        else:
            dict_item.cleaned_value = dict_item.value

        dict_item.save()
