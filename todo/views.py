from django.http import HttpResponse
from django.http import Http404
from django.utils.translation import gettext_lazy as _gtl

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import (
    extend_schema, OpenApiParameter,
)

from todo.models import TodoUser, TodoItem
from todo.serializers import (
    TodoUserDetailSerializer, TodoUserSerializer,
    TodoItemSerializer,
)


def index(request):
    return HttpResponse(
        "Hello, world. You're at the 4Geeks Playground root!"
    )


class TodoUsersViewSet(ReadOnlyModelViewSet):
    __doc__ = _gtl("""
    GTL test
    """)
    queryset = TodoUser.objects.all()
    serializer_class = TodoUserSerializer


class TodoUserDetailViewSet(ModelViewSet):
    serializer_class = TodoUserDetailSerializer

    def get_queryset(self, name):
        try:
            return TodoUser.objects.get(name=name)
        except TodoUser.DoesNotExist:
            raise Http404

    @extend_schema(
        auth=None,
        operation_id="User Details"
    )
    def retrieve(self, request, name, format=None):
        """
        Returns an array of all Todo list users.
        """
        user = self.get_object(name)
        serializer = TodoUserDetailSerializer(
            user,
            context={
                'request': request,
                'name': user.name,
            }
        )
        return Response(serializer.data)

    @extend_schema(
        auth=None,
        operation_id="Delete User"
    )
    def destroy(self, request, name, format=None):
        """
        Allows a user to be deleted.
        """
        todo_user = self.get_object(name)
        todo_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoItemDetailViewSet(ModelViewSet):
    serializer_class = TodoItemSerializer

    def get_object(self, pk):
        try:
            return TodoItem.objects.get(name=pk)
        except TodoItem.DoesNotExist:
            raise Http404

    def update(self, request, pk, format=None):
        """
        Lets a user update a particular todo.
        """
        snippet = self.get_object(pk)
        serializer = TodoItemSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, name, format=None):
        """
        Lets a user delete a particular todo.
        """
        todo_user = self.get_object(name)
        todo_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoItemView(APIView):
    def post(self, request, format=None):
        """
        Allows a user to create a new Todo item.
        """
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
        """
        Returns an array of all Todo items from a particular user.
        """
        user = self.get_object(name)
        serializer = TodoItemSerializer(
            user.todos,
            many=True
        )
        return Response(serializer.data)
