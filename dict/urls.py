from django.urls import path
from . import views
urlpatterns = [
    path('', views.dictionary, name='dictionary'),
    path('item/<int:pk>', views.DictItemDetailView.as_view(), name='dict_item')
]
