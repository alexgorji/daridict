from .model_helpers import remove_spaces, remove_short_vowels, translate_to_sorting_value
from .models import DictItem, DictEntry, DictLanguage


def delete_all_entries():
    for entry in DictEntry.objects.all():
        entry.delete()


def create_entries(item_dari, item_farsi, item_german):
    dari = DictLanguage.objects.get_or_create(value='Dari')[0]
    farsi = DictLanguage.objects.get_or_create(value='Farsi')[0]
    german = DictLanguage.objects.get_or_create(value='German')[0]

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


def fill_cleaned_values():
    for dict_item in DictItem.objects.all():
        dict_item.cleaned_value = remove_spaces(dict_item.value)
        if dict_item.language.value in ['Dari', 'Farsi']:
            dict_item.cleaned_value = remove_short_vowels(dict_item.cleaned_value)

        dict_item.save()


def fill_sorting_values():
    for dict_item in DictItem.objects.all():
        dict_item.sorting_value = translate_to_sorting_value(dict_item.cleaned_value.lower())
        dict_item.save()


def remove_empty_items():
    for entry in DictEntry.objects.all():
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


def get_or_create_item(value, language):
    language = DictLanguage.objects.get(value=language)
    return DictItem.objects.get_or_create(value=value, language=language)
