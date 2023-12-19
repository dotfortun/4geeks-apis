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
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView,
    SpectacularSwaggerView
)

from todo import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test_task, name="cel-test"),
    path(
        'schema/',
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
        'users/',
        views.TodoUsersViewSet.as_view({
            'get': 'list'
        }),
    ),
    path(
        'user/<str:name>/',
        views.TodoUserDetailViewSet.as_view({
            'get': 'retrieve',
            'delete': 'destroy'
        }),
        name="user-details",
    ),
    path(
        'user/<str:name>/todos/',
        views.UserTodoView.as_view(),
        name="user-todos",
    ),
    path(
        'api/todo/',
        views.TodoItemView.as_view()
    ),
    path(
        'todo/<int:pk>/',
        views.TodoItemDetailViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        })
    ),
]
