from django.forms import ModelForm, CharField, TextInput, ModelChoiceField

from .models import Author, Quote


# from django import forms


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=100, required=True, widget=TextInput())
    born_date = CharField(min_length=3, max_length=100, required=True, widget=TextInput())
    born_location = CharField(min_length=3, max_length=100, required=True, widget=TextInput())
    description = TextInput()

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    quote = TextInput()
    author = ModelChoiceField(queryset=Author.objects.all(), required=True)

    class Meta:
        model = Quote
        fields = ['quote', 'author']
        exclude = ['tags']
