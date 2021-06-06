from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.new_post, name='new_post'),
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('<str:username>/<int:post_id>/edit/', views.edit_post, name='edit'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
]
