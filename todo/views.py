from django.http import HttpResponse
from django.http import Http404
from django.utils.translation import gettext_lazy as _gtl

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, mixins, generics

from drf_spectacular.utils import (
    extend_schema,
)

from todo.models import TodoUser, TodoItem
from todo.serializers import (
    TodoUserDetailSerializer, TodoUserSerializer,
    TodoItemSerializer,
)

from .tasks import clean_todos


def index(request):
    return HttpResponse(
        "Hello, world. You're at the 4Geeks Playground root!"
    )


def test_task(request):
    r = clean_todos()
    return HttpResponse(
        "Ding!"
    )


@extend_schema(
    tags=["User Operations"]
)
class TodoUsersViewSet(viewsets.ModelViewSet):
    __doc__ = _gtl("""
    Returns a list of all users.
    """)
    queryset = TodoUser.objects.all()
    serializer_class = TodoUserSerializer

    @extend_schema(
        auth=None,
        operation_id="Create a user"
    )
    def create(self, request):
        """
        Creates a Todo API User.
        """
        user, created = TodoUser.objects.get_or_create(request.data)

        if created:
            serializer = TodoUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                {"msg": "User already exists"},
                400
            )


@extend_schema(
    tags=["User Operations"]
)
class TodoUserDetailViewSet(viewsets.ModelViewSet):
    serializer_class = TodoUserDetailSerializer

    def get_queryset(self, username):
        try:
            return TodoUser.objects.get(username=username)
        except TodoUser.DoesNotExist:
            raise Http404

    @extend_schema(
        auth=None,
        operation_id="Create Todo",
        tags=["Todo Item Operations"],
        request=TodoItemSerializer,
        responses=TodoItemSerializer,
    )
    def create(self, request, username):
        """
        Creates a Todo for a specific user.
        """
        user = TodoUser.objects.get(username=username)
        todo = TodoItemSerializer(
            None, data={
                **request.data,
                "user": user.id
            }
        )
        todo.user = user

        if todo.is_valid():
            todo_item = TodoItem.objects.create(
                **todo.data,
                user=user,
            )
            todo_item.save()
            return Response(TodoItemSerializer(todo_item).data)
        return Response(
            todo.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        auth=None,
        operation_id="Get User Details"
    )
    def retrieve(self, request, username, format=None):
        """
        Returns a specific Todo User object.
        """
        user = self.get_object(username)
        serializer = TodoUserDetailSerializer(
            user,
            context={
                'request': request,
                'username': user.username,
            }
        )
        return Response(serializer.data)

    @extend_schema(
        auth=None,
        operation_id="Delete User"
    )
    def destroy(self, request, username, format=None):
        """
        Allows a user to be deleted.
        """
        todo_user = self.get_object(username)
        todo_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Todo Item Operations"]
)
class TodoItemDetailViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TodoItemSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return TodoItem.objects.filter(pk=pk)


@extend_schema(
    tags=["User Operations"]
)
class UserTodoView(APIView):
    def get_object(self, username):
        try:
            return TodoUser.objects.get(username=username)
        except TodoUser.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        """
        Returns an array of all Todo items from a particular user.
        """
        user = self.get_object(username)
        serializer = TodoItemSerializer(
            user.todos,
            many=True
        )
        return Response(serializer.data)
