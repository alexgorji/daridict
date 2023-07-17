from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_and_update_entries, name='dictionary'),
    path('entry/<int:pk>/edit', views.dict_entry_update_view, name='entry_update'),
    path('nodes/', views.dictionary, name='nodes'),
    path('item/<int:pk>/', views.DictItemDetailView.as_view(), name='dict_item'),
    path('item/<int:pk>/edit', views.DictItemUpdateView.as_view(), name='dict_item_update'),
    path('language/<int:pk>/', views.DictLanguageDetailView.as_view(), name='dict_language'),
    path('node/<int:pk>/edit', views.dict_node_update_view, name='dict_node_update'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
]
