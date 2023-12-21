from rest_framework import serializers

from todoapi.models import TodoUser, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    default_error_messages = {

    }

    label = serializers.CharField(
        max_length=256,
        required=False
    )
    is_done = serializers.BooleanField(
        required=False,
        default=False
    )

    class Meta:
        model = TodoItem
        fields = [
            'id', 'label', 'is_done',
            'created', 'updated'
        ]
        read_only_fields = ['id', 'created', 'updated']


class TodoUserSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(
        read_only=True
    )

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
