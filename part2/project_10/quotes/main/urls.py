from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('add_author/', views.add_new_author, name = 'add_author'),
    path('add_quote/', views.add_new_quote, name = 'add_quote')
]