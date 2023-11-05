from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_and_update_entries, name='dictionary'),
    path('item/<int:pk>/', views.DictItemDetailView.as_view(), name='dict_item'),
    path('item/<int:pk>/edit', views.DictItemUpdateView.as_view(), name='dict_item_update'),
    path('language/<int:pk>/', views.DictLanguageDetailView.as_view(), name='dict_language'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('history', views.show_and_delete_history, name='history'),
    path('sources', views.SourceListView.as_view(), name='source_list'),
    path('sources/create', views.SourceCreateView.as_view(), name='source_create'),
    path('update_session', views.update_session, name='update_session')
]
