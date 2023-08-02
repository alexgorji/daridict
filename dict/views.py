from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import generic

from .forms import DictItemForm, DictItemUpdateForm, DictEntrySortingForm, TagForm
from .model_helpers import remove_redundant_spaces, remove_short_vowels
from .models import DictItem, DictLanguage, DictNode, Tag, DictEntry
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

sorted_by = 'Dari'

persian_letters = ['آ', 'ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط',
                   'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی']


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def show_and_update_entries(request):
    global sorted_by
    dict_languages = DictLanguage.objects.all()
    item_forms = [
        DictItemForm(initial={'language': language}, auto_id=f"{language.value.lower()}_%s",
                     language=language.value)
        for language in dict_languages]
    entry_save_display = 'show'
    entry_copy_display = 'hide'
    entry_update_display = 'hide'
    entry_cancel_display = 'hide'
    number_of_entries_per_page = 50

    if request.method == 'POST':
        if request.user.is_authenticated:
            selected_entry_id = request.POST.get('selected_entry_id')
            selected_entry = None
            if selected_entry_id == "":
                selected_entry_id = None

            if selected_entry_id:
                selected_entry = DictEntry.objects.get(id=selected_entry_id)

            if request.POST.get('entry-delete', None):
                selected_entry.delete()
                return redirect('dictionary')
            else:
                values = request.POST.getlist('value')
                if len(set(values)) == 1 and "" in set(values):
                    pass
                else:
                    items = [None if value == "" else DictItem.objects.get_or_create(value=value, language=language)[0]
                             for
                             value, language in zip(values, dict_languages)]
                    if request.POST.get('entry-update', None):
                        selected_entry.item_dari = items[0]
                        selected_entry.item_farsi = items[1]
                        selected_entry.item_german = items[2]
                        selected_entry.save()
                    elif request.POST.get('entry-copy', None):
                        DictEntry.objects.get_or_create(item_dari=items[0], item_farsi=items[1], item_german=items[2])
    elif request.method == 'GET':
        search_value = request.GET.get('search', '')
        new_sorted_by = request.GET.get('sorted_by', None)
        if new_sorted_by:
            sorted_by = new_sorted_by
        sorting_form = DictEntrySortingForm(initial={'sorted_by': sorted_by})

        if search_value != '':
            queried_entries = DictEntry.objects.all().filter(
                Q(item_dari__cleaned_value__istartswith=search_value) |
                Q(item_farsi__cleaned_value__istartswith=search_value) |
                Q(item_german__cleaned_value__istartswith=search_value)
            ).order_by(f'item_{sorted_by.lower()}__sorting_value')
        else:
            queried_entries = DictEntry.objects.all().order_by(f'item_{sorted_by.lower()}__sorting_value')
        paginator = Paginator(queried_entries, number_of_entries_per_page)

        number_of_pages = paginator.num_pages
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
            elif 'entry_id' in request.GET and request.user.is_authenticated:
                entry_id = request.GET['entry_id']
                if 'edit' in request.GET:
                    entry_save_display = 'hide'
                    entry_copy_display = 'hide'
                    entry_update_display = 'show'
                    entry_cancel_display = 'show'
                elif 'copy' in request.GET:
                    entry_save_display = 'hide'
                    entry_copy_display = 'show'
                    entry_update_display = 'hide'
                    entry_cancel_display = 'show'
                else:
                    pass
                if entry_id != '':
                    entry = DictEntry.objects.get(id=entry_id)
                    item_forms = [DictItemForm(initial={'value': value},
                                               auto_id=f"{language}_%s",
                                               language=language.value)
                                  for language, value in entry.get_ordered_item_attributes().items()]
                else:
                    item_forms = [DictItemForm(auto_id=f"{language}_%s",
                                               language=language.value)
                                  for language in DictLanguage.objects.all()]
                return render(request, 'dict/ajax_entry_form.html',
                              {'selected_entry_id': entry_id,
                               'item_forms': item_forms,
                               'entry_save_display': entry_save_display,
                               'entry_copy_display': entry_copy_display,
                               'entry_update_display': entry_update_display,
                               'entry_cancel_display': entry_cancel_display,
                               }
                              )
            elif 'cancel' in request.GET and request.user.is_authenticated:
                output = render(request, 'dict/ajax_entry_form.html', {
                    'item_forms': item_forms,
                    'selected_entry': None,
                    'entry_save_display': entry_save_display,
                    'entry_copy_display': entry_copy_display,
                    'entry_update_display': entry_update_display,
                    'entry_cancel_display': entry_cancel_display,
                })
                return output

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
                'entry_copy_display': entry_copy_display,
                'entry_update_display': entry_update_display,
                'entry_cancel_display': entry_cancel_display,
                'search_value': search_value
            })


@login_required
def dict_entry_update_view(request, pk):
    entry = DictEntry.objects.get(pk=pk)

    def get_language_value(language):
        for item in entry.get_ordered_items():
            if item and item.language == language:
                return item.value
        return ""

    item_forms = [
        DictItemForm(initial={'language': language, 'value': get_language_value(language)}, auto_id=f"{language}_%s",
                     language=language.value)
        for language in DictLanguage.objects.all()]

    # tags_form = TagForm(initial={'tags': ", ".join(entry.get_tag_names())})

    context = {
        'entry': entry,
        'item_forms': item_forms,
        # 'tags_form': tags_form
    }

    if request.method == 'POST':
        delete_me = request.POST.get('delete', None)
        save_me = request.POST.get('save', None)
        update_me = request.POST.get('update', None)
        # tags = list(set(request.POST.get('tags', None).split(', ')))
        if delete_me:
            entry.delete()
            return redirect('dictionary')
        elif save_me or update_me:
            values = request.POST.getlist('value')
            if len(set(values)) == 1 and "" in set(values):
                pass
            else:
                items = []
                languages = DictLanguage.objects.all()
                for language, value in zip(languages, values):
                    items.append(DictItem.objects.get_or_create(language=language, value=value)[0])
                if items:
                    entry.edit_items(items)
            return redirect('dictionary')

    return render(request, 'dict/dictentry_form.html', context)


class DictEntryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DictEntry
    fields = ['item_dari', 'item_farsi', 'item_german']

    # form_class = DictItemUpdateForm

    def post(self, request, *args, **kwargs):
        delete_me = request.POST.get('delete')
        if delete_me:
            self.get_object().delete()
            return redirect('dictionary')

        return super().post(request, *args, **kwargs)


@login_required
def dictionary(request):
    global sorted_by
    filter_by_tags = []
    initial_filter_by_tags = ''
    if request.method == 'POST':
        del_node_id = request.POST.get('delNodeId', None)
        new_sorted_by = request.POST.get('sorted_by', None)
        tags = request.POST.get('tags', None)
        if tags:
            tags = list(set(tags.split(', ')))
        else:
            tags = []
        filter_by_tags = request.POST.get('filter_by_tags', None)
        if filter_by_tags:
            initial_filter_by_tags = filter_by_tags
            filter_by_tags = list(set(filter_by_tags.split(', ')))
        else:
            filter_by_tags = []
        if del_node_id:
            DictNode.objects.filter(id=del_node_id).delete()
        elif new_sorted_by:
            sorted_by = new_sorted_by
        else:
            values = request.POST.getlist('value')
            if len(set(values)) == 1 and "" in set(values):
                pass
            else:
                languages = request.POST.getlist('language')
                items = []
                for language_id, value in zip(languages, values):
                    items.append(DictItem.objects.get_or_create(language_id=language_id, value=value)[0])
                if items:
                    edit_node_id = request.POST.get('editNodeId', None)
                    if edit_node_id:
                        current_node = DictNode.objects.get(id=edit_node_id)
                        current_node.edit_items(items)
                        current_node.edit_tags(tags)
                    else:
                        node = DictNode.objects.create()
                        for item in items:
                            node.items.add(item)
                        node.edit_tags(tags)
                        node.save()

    item_forms = [DictItemForm(initial={'language': language}, auto_id=f"{language}_%s") for language in
                  DictLanguage.objects.all()]
    sorting_form = DictEntrySortingForm(initial={'sorted_by': sorted_by})
    tag_form = TagForm()
    dict_languages = DictLanguage.objects.all()
    dict_nodes = DictNode.objects.all()
    while filter_by_tags:
        dict_nodes = dict_nodes.filter(tags__name=filter_by_tags.pop())
    # dict_nodes = sorted(dict_nodes, key=lambda x: x.get_language_item(sorted_by).value.lower())
    dict_language_items_json = DictItem.get_language_items_json()
    dict_pk_items_json = DictItem.get_pk_items_json()
    dict_node_json = serializers.serialize('json', DictNode.objects.all())
    tags_pk_tag_json = Tag.pk_tag_json()
    return render(request, 'dict/dictionary.html',
                  {'dict_languages': dict_languages,
                   'dict_nodes': dict_nodes,
                   'dict_item_formset': item_forms,
                   'dict_language_items_json': dict_language_items_json,
                   'dict_pk_items_json': dict_pk_items_json,
                   'dict_node_json': dict_node_json,
                   'tags_pk_tag_json': tags_pk_tag_json,
                   'sorting_form': sorting_form,
                   'tag_form': tag_form,
                   'sorted_by': sorted_by,
                   'initial_filter_by_tags': initial_filter_by_tags
                   })


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


@login_required
def dict_node_update_view(request, pk):
    dictnode = DictNode.objects.get(pk=pk)

    def get_language_value(language):
        for item in dictnode.items.all():
            if item.language == language:
                return item.value
        return ""

    item_forms = [
        DictItemForm(initial={'language': language, 'value': get_language_value(language)}, auto_id=f"{language}_%s")
        for language
        in
        DictLanguage.objects.all()]
    tags_form = TagForm(initial={'tags': ", ".join(dictnode.get_tag_names())})

    context = {
        'dictnode': dictnode,
        'item_forms': item_forms,
        'tags_form': tags_form
    }

    if request.method == 'POST':
        delete_me = request.POST.get('delete', None)
        save_me = request.POST.get('save', None)
        tags = list(set(request.POST.get('tags', None).split(', ')))
        if delete_me:
            dictnode.delete()
            return redirect('dictionary')
        elif save_me:
            values = request.POST.getlist('value')
            if len(set(values)) == 1 and "" in set(values):
                pass
            else:
                languages = request.POST.getlist('language')
                items = []
                for language_id, value in zip(languages, values):
                    items.append(DictItem.objects.get_or_create(language_id=language_id, value=value)[0])
                if items:
                    dictnode.edit_items(items)
                    dictnode.edit_tags(tags)
            return redirect('dictionary')

    return render(request, 'dict/dictnode_form.html', context)


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag
