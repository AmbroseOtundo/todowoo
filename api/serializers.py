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
        fields = ['title', 'memo', 'created', 'datecompleted', 'important']