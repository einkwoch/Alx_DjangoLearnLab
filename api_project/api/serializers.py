from rest_framework import serializers
from .models import Book, Person

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'title',
            'author',
        )


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'title',
            'first_name',
            'last_name',
            'occupation',
        )