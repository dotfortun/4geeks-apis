from django.http import HttpResponse
from django.http import Http404
from django.utils.translation import gettext_lazy as gtl

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from todo.models import TodoUser, TodoItem
from todo.serializers import (
    TodoUserDetailSerializer, TodoUserSerializer,
    TodoItemSerializer,
)


def index(request):
    return HttpResponse(
        "Hello, world. You're at the 4Geeks Playground root!"
    )


class TodoUsersView(APIView):
    def get(self, req, format="none"):
        __doc__ = gtl("""
        Returns an array of all Todo list users.
        """)
        todo_users = TodoUser.objects.all()
        serializer = TodoUserSerializer(todo_users, many=True)
        return Response(serializer.data)


class TodoUserDetail(APIView):
    def get_object(self, name):
        try:
            return TodoUser.objects.get(name=name)
        except TodoUser.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        user = self.get_object(name)
        serializer = TodoUserDetailSerializer(user)
        return Response(serializer.data)

    def delete(self, request, name, format=None):
        todo_user = self.get_object(name)
        todo_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoItemDetail(APIView):
    def get_object(self, pk):
        try:
            return TodoItem.objects.get(name=pk)
        except TodoItem.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TodoItemSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        todo_user = self.get_object(name)
        todo_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoItemView(APIView):
    def post(self, request, format=None):
        serializer = TodoItemSerializer(
            None, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserTodoView(APIView):
    def get_object(self, name):
        try:
            return TodoUser.objects.get(name=name)
        except TodoUser.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        user = self.get_object(name)
        serializer = TodoItemSerializer(
            user.todos,
            many=True
        )
        return Response(serializer.data)
