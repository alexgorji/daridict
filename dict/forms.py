from django import forms

from dict.models import DictItem, DictLanguage, Tag


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
        fields = ['value', 'comment', 'comment_source']


class TagForm(forms.Form):
    class Meta:
        model = Tag
        fields = ['name']


class DictEntrySortingForm(forms.Form):
    sorted_by = forms.ChoiceField(
        choices=lambda: DictLanguage.objects.values_list('value', 'value'),
    )


class DictSearchLanguageForm(forms.Form):
    search_language = forms.ChoiceField(
        label="",
        choices=lambda: DictLanguage.objects.values_list('value', 'abbreviation'),
    )
