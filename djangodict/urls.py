"""taxdocumentmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
import dict.views as dict_view
import home.views as home_view
import profiles.views as profile_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', home_view.home, name='home'),
              ] + [
                  path('login', LoginView.as_view(template_name='profiles/login.html'), name='profiles_login'),
                  path('logout', LogoutView.as_view(template_name='profiles/logged_out.html'), name='profiles_logout'),
                  path('register', profile_views.register, name='profiles_register'),
                  path('<int:pk>/', profile_views.ProfileDetailView.as_view(), name='profiles_detail'),
                  path('<int:pk>/update', profile_views.ProfileUpdateView.as_view(), name='profiles_update'),
                  path('<int:pk>/delete', profile_views.ProfileDeleteView.as_view(), name='profiles_delete'),
              ]
# ] + [
#     path('<int:owner_pk>/taxreturns/', taxreturns_views.TaxReturnListView.as_view(),
#          name='taxreturns_list'),
#     path('<int:owner_pk>/taxreturns/create', taxreturns_views.TaxReturnCreateView.as_view(),
#          name='taxreturns_create'),
#     path('<int:owner_pk>/taxreturns/<int:pk>/', taxreturns_views.TaxReturnDetailView.as_view(),
#          name='taxreturns_detail'),
#     path('<int:owner_pk>/taxreturns/<int:pk>/update', taxreturns_views.TaxReturnUpdateView.as_view(),
#          name='taxreturns_update'),
#     path('<int:owner_pk>/taxreturns/<int:pk>/delete', taxreturns_views.TaxReturnDeleteView.as_view(),
#          name='taxreturns_delete'),
# ] + [
#
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/items/', items_views.ItemListView.as_view(),
#          name='items_list'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/items/create',
#          items_views.ItemCreateView.as_view(), name='items_create'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/items/<int:pk>/',
#          items_views.ItemDetailView.as_view(),
#          name='items_detail'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/items/<int:pk>/update',
#          items_views.ItemUpdateView.as_view(),
#          name='items_update'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/items/<int:pk>/delete',
#          items_views.ItemDeleteView.as_view(),
#          name='items_delete'),
# ] + [
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/categories/',
#          categories_views.CategoryListView.as_view(), name='categories_list'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/categories/<int:pk>/',
#          categories_views.CategoryDetailView.as_view(), name='categories_detail'),
#     # path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/categories/<int:pk>/create',
#     #      categories_views.CategoryCreateView.as_view(), name='categories_create'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/categories/create',
#          categories_views.CategoryCreateView.as_view(), name='categories_create'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/categories/<int:pk>/update',
#          categories_views.CategoryUpdateView.as_view(), name='categories_update'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/categories/<int:pk>/delete',
#          categories_views.CategoryDeleteView.as_view(), name='categories_delete'),
# ] + [
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/documents/',
#          documents_views.DocumentListView.as_view(), name='documents_list'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/documents/create',
#          documents_views.DocumentCreateView.as_view(), name='documents_create'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/documents/<int:pk>/',
#          documents_views.DocumentDetailView.as_view(), name='documents_detail'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/documents/<int:pk>/update',
#          documents_views.DocumentUpdateView.as_view(), name='documents_update'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/documents/<int:pk>/delete',
#          documents_views.DocumentDeleteView.as_view(), name='documents_delete'),
#     path('<int:owner_pk>/taxreturns/<int:taxreturn_pk>/documents/<int:pk>/show-file',
#          documents_views.show_document_file, name='documents_show_file'),
# ]
