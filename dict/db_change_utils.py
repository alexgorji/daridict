from dict.models import DictItem


def find_and_replace_german_genus():
    for item in DictItem.objects.filter(language__value='German'):
        item.value = item.value.replace('(r)', '(m)')
        item.value = item.value.replace('(e)', '(f)')
        item.value = item.value.replace('(s)', '(n)')
        item.save()