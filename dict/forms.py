from django import forms

from dict.models import DictItem, DictLanguage, Tag, DictEntry


class DictItemForm(forms.ModelForm):
    class Meta:
        model = DictItem
        fields = ['value']

    def __init__(self, *args, **kwargs):
        language = None
        try:
            language = kwargs.pop('language')
        except KeyError:
            pass

        super().__init__(*args, **kwargs)
        self.fields['value'].widget.attrs['placeholder'] = language
        self.fields['value'].label = language


class DictItemUpdateForm(forms.ModelForm):
    class Meta:
        model = DictItem
        fields = ['value', 'comment']


class TagForm(forms.Form):
    class Meta:
        model = Tag
        fields = ['name']


class DictEntrySortingForm(forms.Form):
    CHOICES = [(language.value, language.value) for language in DictLanguage.objects.all()]
    sorted_by = forms.ChoiceField(choices=CHOICES)


class DictEntryApprovedForm(forms.ModelForm):
    class Meta:
        model = DictEntry
        fields = ['approved']
