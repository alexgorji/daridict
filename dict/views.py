from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render, redirect
from django.views import generic

from .forms import DictItemForm, DictItemUpdateForm, DictNodesSortingForm
from .models import DictItem, DictLanguage, DictNode

sorted_by = 'Dari'


@login_required
def dictionary(request):
    global sorted_by
    if request.method == 'POST':
        del_node_id = request.POST.get('delNodeId', None)
        new_sorted_by = request.POST.get('sorted_by', None)
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
                    else:
                        node = DictNode.objects.create()
                        for item in items:
                            node.items.add(item)
                        node.save()

    item_forms = [DictItemForm(initial={'language': language}, auto_id=f"{language}_%s") for language in
                  DictLanguage.objects.all()]
    sorting_form = DictNodesSortingForm(initial={'sorted_by': sorted_by})
    dict_languages = DictLanguage.objects.all()
    dict_nodes = sorted(DictNode.objects.all(), key=lambda x: x.get_language_item(sorted_by).value.lower())
    dict_language_items_json = DictItem.get_language_items_json()
    dict_pk_items_json = DictItem.get_pk_items_json()
    dict_node_json = serializers.serialize('json', DictNode.objects.all())
    return render(request, 'dict/dictionary.html',
                  {'dict_languages': dict_languages,
                   'dict_nodes': dict_nodes,
                   'dict_item_formset': item_forms,
                   'dict_language_items_json': dict_language_items_json,
                   'dict_pk_items_json': dict_pk_items_json,
                   'dict_node_json': dict_node_json,
                   'sorting_form': sorting_form,
                   'sorted_by': sorted_by
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

    item_forms = [DictItemForm(initial={'language': language, 'value': get_language_value(language)}, auto_id=f"{language}_%s") for language
                  in
                  DictLanguage.objects.all()]
    context = {
        'dictnode': dictnode,
        'item_forms': item_forms
    }

    if request.method == 'POST':
        delete_me = request.POST.get('delete', None)
        save_me = request.POST.get('save', None)
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
            return redirect('dictionary')
            # for language_id, value in zip(languages, values):
            #     items.append(DictItem.objects.get_or_create(language_id=language_id, value=value)[0])

    return render(request, 'dict/dictnode_form.html', context)
