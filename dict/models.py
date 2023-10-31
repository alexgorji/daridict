from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from dict.model_helpers import remove_redundant_spaces, remove_short_vowels, translate_to_sorting_value


class DictLanguage(models.Model):
    value = models.CharField(max_length=20, blank=False, unique=True)
    history = HistoricalRecords()
    LTR = 'LTR'
    RTL = 'RTL'
    SOPHOMORE = 'SO'
    DIRECTION_CHOICES = [
        (LTR, 'ltr'),
        (RTL, 'rtf'),
    ]

    direction = models.CharField(
        max_length=3,
        choices=DIRECTION_CHOICES,
        default=LTR,
    )

    def __str__(self):
        return self.value

    def get_sorted_items(self):
        return self.dictitem_set.all().order_by('sorting_value')

    class Meta:
        ordering = ['id']


class DictItem(models.Model):
    language = models.ForeignKey(to=DictLanguage, on_delete=models.RESTRICT)
    value = models.CharField(max_length=250, blank=False)
    cleaned_value = models.CharField(max_length=250, blank=False)
    sorting_value = models.CharField(max_length=250, blank=False)
    comment = models.TextField(blank=True)
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language', 'value'], name='unique value in language')
        ]
        ordering = ['value']

    def __str__(self):
        return f"{self.id}: {self.language.value}: {self.value}"

    def get_absolute_url(self):
        return reverse('dict_item', kwargs={'pk': self.pk})

    def get_entries(self):
        if self.language.value == 'Dari':
            return self.entry_dari_item.all()
        elif self.language.value == 'Farsi':
            return self.entry_farsi_item.all()
        elif self.language.value == 'German':
            return self.entry_german_item.all()
        else:
            raise NotImplementedError(f'language: {self.language.value} is not an entry language.')

    def save(self, *args, **kwargs):
        self.cleaned_value = remove_redundant_spaces(self.value)
        self.cleaned_value = remove_short_vowels(self.cleaned_value)
        self.sorting_value = translate_to_sorting_value(self.cleaned_value.lower())
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.fields.CharField(max_length=30, unique=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'tag {self.id}: {self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        return super().save(*args, **kwargs)


class DictSource(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    url = models.URLField(max_length=300, blank=True)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('source_list')

    def __str__(self):
        return self.name


class DictEntry(models.Model):
    item_dari = models.ForeignKey(to='dict.DictItem', blank=True, on_delete=models.RESTRICT,
                                  related_name='entry_dari_item',
                                  null=True)
    item_farsi = models.ForeignKey(to='dict.DictItem', blank=True, on_delete=models.RESTRICT,
                                   related_name='entry_farsi_item',
                                   null=True)
    item_german = models.ForeignKey(to='dict.DictItem', blank=True, on_delete=models.RESTRICT,
                                    related_name='entry_german_item',
                                    null=True)
    order_of_languages = ['German', 'Farsi', 'Dari']
    order_of_items = [f'item_{language.lower()}' for language in order_of_languages]
    tags = models.ManyToManyField(to=Tag, blank=True)
    sources = models.ManyToManyField(to=DictSource, blank=True)
    approved = models.BooleanField(default=False)
    history = HistoricalRecords(m2m_fields=[tags, sources])

    def __str__(self):
        try:
            items = [item.value if item else '___' for item in self.get_ordered_items()]
            return f'{self.id}: {" - ".join(items)}'
        except DictItem.DoesNotExist:
            return f'{self.id}: item(s) deleted'

    @property
    def simple_string(self):
        items = [item.value if item else '___' for item in self.get_ordered_items()]
        return " - ".join(items)

    def edit_items(self, items):
        items = [item if item != '' else None for item in items]
        for self_item, item in zip(self.order_of_items, items):
            setattr(self, self_item, item)
        self.save()

    def get_approved(self):
        if self.approved:
            if self.sources.all():
                return 'approved: ' + self.get_sources_as_string()
            return 'approved'
        else:
            return 'not approved'

    def get_ordered_items(self):
        return [getattr(self, item) for item in self.order_of_items]

    def get_ordered_item_attributes(self):
        return {language: item.value if item else '' for language, item in
                zip([DictLanguage.objects.get(value=lang) for lang in self.order_of_languages],
                    self.get_ordered_items())}

    def get_sources_as_string(self) -> str:
        return ', '.join([source.name for source in self.sources.all().order_by('name')])

    def get_tags_as_string(self) -> str:
        return ", ".join([tag.name for tag in self.tags.all().order_by('name')])

    @staticmethod
    def get_ordered_languages():
        return [DictLanguage.objects.get(value=language) for language in DictEntry.order_of_languages]
