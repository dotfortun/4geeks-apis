"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView,
    SpectacularSwaggerView
)

from todo import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='redoc'
    ),
    path(
        'api/users/',
        views.TodoUsersView.as_view()
    ),
    path(
        'api/user/<str:name>/',
        views.TodoUserDetail.as_view(),
        name="user-todos"
    ),
    path(
        'api/user/<str:name>/todos/',
        views.UserTodoView.as_view()
    ),
    path(
        'api/todo/',
        views.TodoItemView.as_view()
    ),
    path(
        'api/todo/<int:pk>/',
        views.TodoItemDetail.as_view()
    ),
]
