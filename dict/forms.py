from django import forms

from dict.models import DictItem, DictNode, DictLanguage


class DictItemForm(forms.ModelForm):
    class Meta:
        model = DictItem
        fields = ['language', 'value']


class DictItemUpdateForm(forms.ModelForm):
    class Meta:
        model = DictItem
        fields = ['value', 'comment']


class DictNodeUpdateForm(forms.ModelForm):
    class Meta:
        model = DictNode
        fields = ['items']


class DictNodesSortingForm(forms.Form):
    CHOICES = [(language.value, language.value) for language in DictLanguage.objects.all()]
    sorted_by = forms.ChoiceField(choices=CHOICES)
