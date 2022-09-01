from rest_framework import serializers
from todo.models import Todo

# This class is a serializer for the Todo model. It will be used to convert the Todo model into JSON
# format
class TodoSerializer(serializers.ModelSerializer):
    # Making the fields read only.
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()
    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created', 'datecompleted', 'important']

# todo api completed
class TodoCompleteSerializer(serializers.ModelSerializer):
    # Making the fields read only.
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title', 'memo', 'created', 'datecompleted', 'important']