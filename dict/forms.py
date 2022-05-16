from django import forms
from django.forms import modelformset_factory

from dict.models import DictItem


class DictItemForm(forms.ModelForm):

    class Meta:
        model = DictItem
        fields = ['language', 'value']

# DictItemFormSet = modelformset_factory(DictItem, fields=('language', 'value'))
