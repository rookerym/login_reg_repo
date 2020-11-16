from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('create_user', views.register),
    path('success', views.success),
    path('login_user', views.login),
    path('create_message', views.create_message),
    path('logout', views.logout),
    path('user/<int:user_id>', views.profile),
    path('create_comment', views.create_comment),
    path('delete_walls/<int:message_id>', views.delete_wallpost),
    path('delete_comm/<int:comment_id>', views.delete_comm),
]