from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from profiles.models import Profile

User = get_user_model()


def create_profile(data):
    user_data = {**data['user']}
    user_data.pop('password2')
    user = User.objects.create_user(**user_data)
    user.save()
    profile_data = {**data['profile']}
    profile_data.update({'user': user})
    person = Profile(**profile_data)
    person.save()
    return person

#
# def create_item(taxreturn, data):
#     data = {'taxreturn': taxreturn, **data}
#     if 'date' not in data:
#         data['date'] = '2020-12-12'
#     if 'sum' not in data:
#         data['sum'] = 100
#     item = Item(**data)
#     item.save()
#     return item


def reverse_profile_view(view_name, profile):
    return reverse(view_name, kwargs={'pk': profile.id})


# def generate_view_kwargs(view_name, object_):
#     if view_name in ['categories_detail', 'categories_delete', 'categories_update',
#                      'documents_detail', 'documents_delete', 'documents_update', 'documents_show_file',
#                      'items_detail', 'items_delete', 'items_update']:
#         return {'owner_pk': object_.taxreturn.owner.pk, 'taxreturn_pk': object_.taxreturn.pk, 'pk': object_.pk}
#     elif view_name in ['categories_create', 'categories_list', 'documents_list', 'documents_create', 'items_list',
#                        'items_create']:
#         return {'owner_pk': object_.owner.pk, 'taxreturn_pk': object_.pk}
#     elif view_name in ['taxreturns_delete', 'taxreturns_update', 'taxreturns_detail']:
#         return {'owner_pk': object_.owner.pk, 'pk': object_.pk}
#     elif view_name in ['taxreturns_list', 'taxreturns_create']:
#         return {'owner_pk': object_.owner.pk}
#     else:
#         raise NotImplementedError
#
#
# def get_view_reverse(view_name, object_):
#     return reverse(view_name, kwargs=generate_view_kwargs(view_name, object_))
#
#
# def reset_settings_categories():
#     for category_setting in ['CATEGORY_ITEM_INCOME', 'CATEGORY_ITEM_EXPENSE', 'CATEGORY_ITEM_CHARITY',
#                              'CATEGORY_ITEM_EXTRAORDINARY', 'CATEGORY_ITEM_EXPENSE_CHILDREN',
#                              'CATEGORY_ITEM_EXPENSE_JOURNEY', 'CATEGORY_ITEM_EXPENSE_JOURNEY_CHILDREN',
#                              'CATEGORY_DOCUMENT_CHILDREN']:
#         try:
#             setattr(settings, category_setting, None)
#         except AttributeError:
#             pass
#     settings.CATEGORY_ITEM_INCOME = 'Income'
#     settings.CATEGORY_ITEM_Expense = 'Expense'
