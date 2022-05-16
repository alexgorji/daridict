from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DictItemForm
from .models import DictItem, DictLanguage, DictNode


# from .forms import DictItemFormSet

# dict_item_formset = DictItemFormSet()


def dictionary(request):
    return render(request, 'dict/dictionary.html', {'dict_nodes': DictNode.objects.all(), 'dict_languages': DictLanguage.objects.all(),
                                                    'dict_item_formset': [DictItemForm(initial={'language': language}) for language in
                                                                          DictLanguage.objects.all()]})


class DictItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = DictItem
