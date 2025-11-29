from rest_framework import serializers
from .models import Book, Author
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    """
    Serializer for the Book model.
    Converts Book model instances into JSON and validates input for creating/updating Books.
    """
    class Meta:
        model = Book
        fields = '__all__'

    This_year = date.today().year
    # Stores the current year (e.g., 2025) as a class attribute.
    # Used in validation to prevent future publication years.

    def validate(self, data):

        """
        Object-level validation.
        Called automatically during serializer.is_valid().
        Validates that 'publication_year' is not in the future.
        """

        if data['publication_year'] > self.This_year:
            # If the book's publication year is greater than the current year,
            # raise a validation error.
            raise serializers.ValidationError("Publication year cannot be in the future")
        return data
        # Return validated data if no errors
    
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes all related books using the nested BookSerializer.
    """
    books = BookSerializer(many=True, read_only=True)
    # Nested serializer.
    # 'many=True' tells DRF that an author can have multiple books.
    # This will automatically serialize the author's related books.
    class Meta:
        model = Author
        fields = (
            'name',
            'books'

        )