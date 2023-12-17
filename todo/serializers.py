from rest_framework import serializers

from todo.models import TodoUser, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = [
            'id',
            'label',
            'is_done',
            'created',
            'updated',
        ]


class TodoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoUser
        fields = [
            'name',
            'created',
        ]


class TodoUserDetailSerializer(serializers.ModelSerializer):
    todos = serializers.HyperlinkedIdentityField(
        view_name="user-todos",
        lookup_field="name",
    )

    class Meta:
        model = TodoUser
        fields = [
            'name',
            'created',
            'todos',
        ]
