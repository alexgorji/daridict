from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_and_update_entries, name='dictionary'),
    path('item/<int:pk>/', views.DictItemDetailView.as_view(), name='dict_item'),
    path('item/<int:pk>/edit', views.DictItemUpdateView.as_view(), name='dict_item_update'),
    path('language/<int:pk>/', views.DictLanguageDetailView.as_view(), name='dict_language'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('entries/<int:pk>/', views.dict_entry_update_view, name='dict_entry_update')
]
