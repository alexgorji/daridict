
from .models import DictItem, DictEntry, DictLanguage


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

    return DictEntry.objects.create(item_dari=item_dari, item_farsi=item_farsi, item_german=item_german)
