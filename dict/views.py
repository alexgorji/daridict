from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, RestrictedError, ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from .forms import DictItemForm, DictItemUpdateForm, DictEntrySortingForm
from .model_helpers import remove_redundant_spaces, remove_short_vowels
# from .models import DictItem, DictLanguage, Tag, DictEntry, HistoricalDictEntry, HistoricalDictItem
from .models import DictItem, DictLanguage, Tag, DictEntry

from django.core.paginator import Paginator

sorted_by = 'Dari'


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def show_and_update_entries(request):
    global sorted_by
    dict_languages = [DictLanguage.objects.get(value=language) for language in DictEntry.order_of_languages]
    item_forms = [
        DictItemForm(initial={'language': language},
                     language=language.value, prefix=language.value.lower())
        for language in dict_languages]
    entry_save_display = 'show'
    entry_update_display = 'hide'
    entry_cancel_display = 'hide'
    number_of_entries_per_page = 50

    if request.method == 'POST':
        def get_post(parameter):
            return request.POST.get(parameter)

        if request.user.is_authenticated:
            selected_entry_id = get_post('selected_entry_id')
            selected_entry = None
            if selected_entry_id == "":
                selected_entry_id = None

            if selected_entry_id:
                selected_entry = DictEntry.objects.get(id=selected_entry_id)

            # delete entry
            if get_post('entry-delete'):
                selected_entry.delete()
                return redirect('dictionary')
            elif get_post('entry-open'):
                return redirect('dict_entry_update', selected_entry_id)

            # AJAX POST requests
            if is_ajax(request):
                # update or save entry
                entry_is_new = False
                values = [get_post(f'{language.lower()}_value') for language in DictEntry.order_of_languages]
                if len(set(values)) == 1 and "" in set(values):
                    pass
                else:
                    items = [None if value == "" else DictItem.objects.get_or_create(value=value, language=language)[0]
                             for
                             value, language in zip(values, dict_languages)]
                    # update entry
                    if request.POST.get('entry-update', None):
                        for item, dict_language in zip(items, dict_languages):
                            setattr(selected_entry, f'item_{dict_language.value.lower()}', item)
                        selected_entry.save()
                    else:
                        # save entry
                        for item, dict_language in zip(items, dict_languages):
                            if dict_language.value == 'Dari':
                                item_dari = item
                            elif dict_language.value == 'Farsi':
                                item_farsi = item
                            elif dict_language.value == 'German':
                                item_german = item
                            else:
                                raise NotImplementedError
                        selected_entry, entry_is_new = DictEntry.objects.get_or_create(item_dari=item_dari,
                                                                                       item_farsi=item_farsi,
                                                                                       item_german=item_german)
                # create or update entry tags
                tag_names = request.POST['tag_names'].split(',')
                # remove redundant emtpy strings
                tag_names = [x.strip() for x in tag_names if x and not x.isspace()]

                tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
                if selected_entry and tag_names != [tag.name for tag in selected_entry.tags.all()]:
                    for tag in selected_entry.tags.all():
                        if tag not in tags:
                            selected_entry.tags.remove(tag)
                    for tag in tags:
                        if tag not in selected_entry.tags.all():
                            selected_entry.tags.add(tag)
                    selected_entry.save()
                if request.POST.get('entry-save', None):
                    if not entry_is_new:
                        return HttpResponse('')
                    return render(request, 'dict/ajax_new_entry.html',
                                  {'entry': selected_entry}
                                  )
                elif request.POST.get('entry-update', None):
                    return render(request, 'dict/ajax_entry_tags_and_items.html',
                                  {'entry': selected_entry}
                                  )
                else:
                    print(request.POST)
    elif request.method == 'GET':
        # get sorted_by and set Sorting Form
        new_sorted_by = request.GET.get('sorted_by', None)
        if new_sorted_by:
            sorted_by = new_sorted_by
        sorting_form = DictEntrySortingForm(initial={'sorted_by': sorted_by})

        # get search value and set entries for paginator
        search_value = request.GET.get('search', '')
        search_tags_value = request.GET.get('tags', '')
        if search_value != '':
            if search_tags_value != '':
                queried_entries = DictEntry.objects.all().filter(
                    (Q(item_dari__cleaned_value__istartswith=search_value) |
                     Q(item_farsi__cleaned_value__istartswith=search_value) |
                     Q(item_german__cleaned_value__istartswith=search_value)) & Q(
                        tags__name__in=search_tags_value.split(', '))
                ).order_by(f'item_{sorted_by.lower()}__sorting_value')
            else:
                queried_entries = DictEntry.objects.all().filter(
                    Q(item_dari__cleaned_value__istartswith=search_value) |
                    Q(item_farsi__cleaned_value__istartswith=search_value) |
                    Q(item_german__cleaned_value__istartswith=search_value)
                ).order_by(f'item_{sorted_by.lower()}__sorting_value')
        else:
            if search_tags_value != '':
                queried_entries = DictEntry.objects.filter(tags__name__in=search_tags_value.split(', ')).order_by(
                    f'item_{sorted_by.lower()}__sorting_value')
            else:
                queried_entries = DictEntry.objects.all().order_by(f'item_{sorted_by.lower()}__sorting_value')
        paginator = Paginator(queried_entries, number_of_entries_per_page)
        number_of_pages = paginator.num_pages
        # AJAX GET requests
        if is_ajax(request):
            if 'page' in request.GET:
                page = request.GET.get('page')
                entries = paginator.page(page)
                return render(request,
                              'dict/ajax_page_entries.html',
                              {'entries': entries,
                               'page': page,
                               'number_of_pages': number_of_pages,
                               'number_of_entries_per_page': number_of_entries_per_page})
            elif 'autocomplete' in request.GET:
                word_beginning = request.GET['autocomplete']
                items = []
                if len(word_beginning) < 2:
                    pass
                else:
                    word_beginning = remove_short_vowels(remove_redundant_spaces(word_beginning)).lower()
                    language = request.GET.get('language')
                    if language:
                        items = [item.value for item in DictItem.objects.filter(language__value=language.capitalize(),
                                                                                cleaned_value__istartswith=word_beginning)]
                    else:
                        items = [item.value for item in
                                 DictItem.objects.filter(cleaned_value__istartswith=word_beginning)]
                        items = list(dict.fromkeys(items))
                return render(request, 'dict/ajax_autocomplete.html', {'items': items})
            elif 'autocompletetags' in request.GET:
                word_beginnings = request.GET['autocompletetags'].split(', ')
                word_beginning = word_beginnings[-1]
                exclude = word_beginnings[:-1]
                items = []
                if len(word_beginning) > 0:
                    items = [tag.name for tag in Tag.objects.filter(name__istartswith=word_beginning)]
                    items = list(set(items).difference(exclude))
                return render(request, 'dict/ajax_autocomplete.html', {'items': items})
            elif 'entry_id' in request.GET and request.user.is_authenticated:
                entry_id = request.GET['entry_id']
                entry = None
                if 'edit' in request.GET:
                    entry_save_display = 'hide'
                    entry_update_display = 'show'
                    entry_cancel_display = 'show'
                elif 'copy' in request.GET:
                    entry_save_display = 'show'
                    entry_update_display = 'hide'
                    entry_cancel_display = 'show'
                else:
                    pass
                if entry_id != '':
                    entry = DictEntry.objects.get(id=entry_id)
                    item_forms = [DictItemForm(initial={'value': value},
                                               prefix=language.value.lower(),
                                               language=language.value)
                                  for language, value in entry.get_ordered_item_attributes().items()]

                else:
                    pass

                return render(request, 'dict/ajax_entry_form.html',
                              {'selected_entry_id': entry_id,
                               'entry': entry,
                               'item_forms': item_forms,
                               'entry_save_display': entry_save_display,
                               'entry_update_display': entry_update_display,
                               'entry_cancel_display': entry_cancel_display,
                               }
                              )
            elif 'cancel' in request.GET and request.user.is_authenticated:
                return render(request, 'dict/ajax_entry_form.html', {
                    'item_forms': item_forms,
                    'selected_entry': None,
                    'entry_save_display': entry_save_display,
                    'entry_update_display': entry_update_display,
                    'entry_cancel_display': entry_cancel_display,
                })

        else:
            return render(request, 'dict/entries.html', {
                'entries': None,
                'dict_languages': dict_languages,
                'sorting_form': sorting_form,
                'number_of_pages': paginator.num_pages,
                'page': 0,
                'number_of_entries_per_page': number_of_entries_per_page,
                'item_forms': item_forms,
                'selected_entry': None,
                'entry_save_display': entry_save_display,
                'entry_update_display': entry_update_display,
                'entry_cancel_display': entry_cancel_display,
                'search_value': search_value,
                'search_tags_value': search_tags_value
            })


@login_required
def dict_entry_update_view(request, pk):
    entry = DictEntry.objects.get(pk=pk)
    item_forms = [DictItemForm(initial={'value': value},
                               auto_id=f"{language.value.lower()}_%s",
                               language=language.value)
                  for language, value in entry.get_ordered_item_attributes().items()]

    context = {
        'entry': entry,
        'item_forms': item_forms,
    }

    if request.method == 'POST':
        if request.POST.get('delete', None):
            entry.delete()
            return redirect('dictionary')
        else:
            values = request.POST.getlist('value')
            if len(set(values)) == 1 and "" in set(values):
                pass
            else:
                items = [None if value == "" else DictItem.objects.get_or_create(value=value, language=language)[0]
                         for
                         value, language in zip(values, entry.get_ordered_languages())]

                for item in items:
                    setattr(entry, f'item_{item.language.value.lower()}', item)
            tag_names = request.POST['tag_names'].split(',')
            tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
            for tag in entry.tags.all():
                if tag not in tags:
                    entry.tags.remove(tag)
            for tag in tags:
                if tag not in entry.tags.all():
                    entry.tags.add(tag)

            entry.save()
        # return redirect('dictionary')
    elif request.method == 'GET':
        if is_ajax(request):
            if 'autocomplete' in request.GET:
                word_beginnings = request.GET['autocomplete'].split(', ')
                word_beginning = word_beginnings[-1]
                exclude = word_beginnings[:-1]
                items = []
                if len(word_beginning) > 0:
                    items = [tag.name for tag in Tag.objects.filter(name__istartswith=word_beginning)]
                    items = list(set(items).difference(exclude))
                return render(request, 'dict/ajax_autocomplete.html', {'items': items})

    return render(request, 'dict/dictentry_form.html', context)


class DictItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = DictItem


class DictItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DictItem
    form_class = DictItemUpdateForm

    def post(self, request, *args, **kwargs):
        delete_me = request.POST.get('delete')
        if delete_me:
            self.get_object().delete()
            return redirect('dictionary')

        return super().post(request, *args, **kwargs)


class DictLanguageDetailView(LoginRequiredMixin, generic.DetailView):
    model = DictLanguage

    def post(self, request, pk):
        if request.POST.get('item-delete'):
            try:
                DictItem.objects.get(id=request.POST.get('selected-item-id')).delete()
            except RestrictedError as err:
                print(err)
        return redirect('dict_language', pk)


class TagListView(generic.ListView):
    model = Tag
    ordering = 'name'

    def post(self, request):
        if request.POST.get('tag-delete'):
            Tag.objects.get(id=request.POST.get('selected-tag-id')).delete()
        return redirect('tag_list')


class TagDetailView(generic.DetailView):
    model = Tag


# def show_history(request):
#     # items_history = HistoricalDictItem.objects.all()
#     entries_history = []
#     HistoricalDictEntry.objects.all()
#     for entry in HistoricalDictEntry.objects.all():
#         try:
#             print(entry)
#             entries_history.append(entry)
#         except DictItem.DoesNotExist as err:
#             print(entry.id, err)
#             entries_history.append(entry.id)
#
#     # for entry in HistoricalDictEntry.objects.all():
#     #     try:
#     #         entries_history.append(entry)
#     #     except Exception as err:
#     #         print(err)
#     #     try:
#     #         entries_history.append(entry)
#     #     except ObjectDoesNotExist:
#     #         print(entry)
#     return render(request, 'dict/history.html',
#                   context={'entries_history': entries_history})
