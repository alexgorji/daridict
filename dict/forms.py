from django import forms

from dict.models import DictItem, DictNode, DictLanguage, Tag


class DictItemForm(forms.ModelForm):
    class Meta:
        model = DictItem
        fields = ['value']

    def __init__(self, *args, **kwargs):
        label = None
        try:
            label = kwargs.pop('label')
        except KeyError:
            pass

        super().__init__(*args, **kwargs)
        self.fields['value'].widget.attrs['placeholder'] = label


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


class TagForm(forms.Form):
    tags = forms.CharField(max_length=500)


class DictEntrySortingForm(forms.Form):
    CHOICES = [(language.value, language.value) for language in DictLanguage.objects.all()]
    sorted_by = forms.ChoiceField(choices=CHOICES)
