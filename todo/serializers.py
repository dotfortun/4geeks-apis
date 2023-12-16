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
    todos = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user-todos',
    )

    class Meta:
        model = TodoUser
        fields = [
            'name',
            'created',
            'todos',
        ]


class TodoUserDetailSerializer(serializers.ModelSerializer):
    todos = TodoItemSerializer(many=True, read_only=True)

    class Meta:
        model = TodoUser
        fields = [
            'name',
            'created',
            'todos',
        ]
