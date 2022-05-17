import json

from django.db import models
from django.db.models.signals import m2m_changed
from django.urls import reverse


class DictNodeLanguageException(Exception):
    def __init__(self, *args):
        message = f"DictNode can only have one item of each language!"
        super().__init__(message, *args)


class DictLanguage(models.Model):
    value = models.CharField(max_length=20, blank=False)

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

    class Meta:
        ordering = ['id']


class DictItem(models.Model):
    language = models.ForeignKey(to=DictLanguage, on_delete=models.CASCADE)
    value = models.CharField(max_length=40, blank=False)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.language.value}: {self.value}"

    @staticmethod
    def get_language_items_json():
        output = {}
        for item in DictItem.objects.all().order_by('language', 'value'):
            key = item.language.value
            if not output.get(key):
                output[key] = []
            output[key].append(item.value)
        return json.dumps(output)

    @staticmethod
    def get_pk_items_json():
        output = {}
        for item in DictItem.objects.all():
            output[item.pk] = [item.language.value, item.value]
        return json.dumps(output)

    def get_absolute_url(self):
        return reverse('dict_item', kwargs={'pk': self.pk})


class DictNode(models.Model):
    items = models.ManyToManyField(to=DictItem, blank=True)

    def __str__(self):
        return f'{self.id}: {" - ".join([item.value for item in self.items.all()])}'

    def get_ordered_items(self):
        return self.items.all().order_by('language_id')

    def get_language_item(self, language):
        return self.items.get(language__value=language)

    def edit_items(self, items):
        for item in self.items.all():
            if item not in items:
                self.items.remove(item)
        for item in items:
            if item not in self.items.all():
                self.items.add(item)
        self.save()


def items_changed(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        languages = [item.language.id for item in instance.items.all()]
        if len(languages) != len(set(languages)):
            raise DictNodeLanguageException


m2m_changed.connect(items_changed, sender=DictNode.items.through)
