from django.db import models
from django.db.models.signals import m2m_changed


class DictNodeLanguageException(Exception):
    def __init__(self, *args):
        message = f"DictNode can only have one item of each language!"
        super().__init__(message, *args)


class DictLanguage(models.Model):
    value = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.value


class DictItem(models.Model):
    language = models.ForeignKey(to=DictLanguage, on_delete=models.CASCADE)
    value = models.CharField(max_length=40, blank=False)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.language.value}: {self.value}"


class DictNode(models.Model):
    items = models.ManyToManyField(to=DictItem, blank=True)

    def __str__(self):
        return f'{self.id}: {self.items.all()}'

    def get_ordered_items(self):
        return self.items.all().order_by('language_id')


def items_changed(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        languages = [item.language.id for item in instance.items.all()]
        if len(languages) != len(set(languages)):
            raise DictNodeLanguageException


m2m_changed.connect(items_changed, sender=DictNode.items.through)
