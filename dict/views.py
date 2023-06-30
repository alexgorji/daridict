from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render, redirect
from django.views import generic

from .forms import DictItemForm, DictItemUpdateForm, DictNodesSortingForm, TagForm
from .models import DictItem, DictLanguage, DictNode, Tag, DictEntry

sorted_by = 'Dari'

persian_letters = ['آ', 'ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط',
                   'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی']


@login_required
def show_entries(request):
    entries = DictEntry.objects.all().order_by(f'item_{sorted_by.lower()}__sorting_value')
    dict_languages = DictLanguage.objects.all()
    # if request.method == 'POST':
    #     print('posting')
    # elif request.method == 'GET':
    #     print(request.GET)
    #     if request.GET.get('persian_alphabet'):
    #         entries = DictEntry.objects.all().order_by(f'item_{sorted_by.lower()}__cleaned_value')
    return render(request, 'dict/entries.html', {
        'entries': entries,
        'dict_languages': dict_languages,
        # 'persian_letters': persian_letters
    })


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
    sorting_form = DictNodesSortingForm(initial={'sorted_by': sorted_by})
    tag_form = TagForm()
    dict_languages = DictLanguage.objects.all()
    dict_nodes = DictNode.objects.all()
    while filter_by_tags:
        dict_nodes = dict_nodes.filter(tags__name=filter_by_tags.pop())
    dict_nodes = sorted(dict_nodes, key=lambda x: x.get_language_item(sorted_by).value.lower())
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
