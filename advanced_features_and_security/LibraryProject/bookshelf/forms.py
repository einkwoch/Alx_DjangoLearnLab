from django import forms
from .models import Book, Author

class ExampleForm(forms.ModelForm):
    title = forms.CharField(max_length=100, strip=True)
    author = forms.ModelChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ["title", "author"]
    
    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        # Optional: basic check against only-whitespace
        if not title:
            raise forms.ValidationError("Title cannot be empty or whitespace.")
        return title

class SearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=100, strip=True)