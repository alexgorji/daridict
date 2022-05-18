from django.urls import path
from . import views

urlpatterns = [
    path('', views.dictionary, name='dictionary'),
    path('item/<int:pk>/', views.DictItemDetailView.as_view(), name='dict_item'),
    path('item/<int:pk>/edit', views.DictItemUpdateView.as_view(), name='dict_item_update'),
    path('language/<int:pk>/', views.DictLanguageDetailView.as_view(), name='dict_language'),
    path('node/<int:pk>/edit', views.dict_node_update_view, name='dict_node_update'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail')
]
