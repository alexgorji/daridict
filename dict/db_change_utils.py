import re

from dict.models import DictItem, DictSource


def find_and_replace_german_genus():
    for item in DictItem.objects.filter(language__value='German'):
        item.value = item.value.replace('(r)', '(m)')
        item.value = item.value.replace('(e)', '(f)')
        item.value = item.value.replace('(s)', '(n)')
        item.save()


def select_comment_source():
    """
    Look into all comments and search for sources. A source is inside parentheses and appears at the end of the
    comment.

    If a source is found it will be made sure that the comment_source of the item has the same value. Then the source
    string will be removed from the comment.

    If source and comment_source diverge no action will be made.
    """
    for item in DictItem.objects.all():
        if item.comment != '':
            re_search = re.search('\((.*)\)$', item.comment)
            if re_search:
                possible_source = re_search.groups()[0]
                source = DictSource.objects.filter(name=possible_source)
                if source:
                    m = re.search('(\(.*\))$', item.comment)
                    item.comment = item.comment[:m.start()] + item.comment[m.end():]
                    item.comment_source = source[0]
                    item.save()
