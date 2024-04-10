from django import forms
from ..models import Author, Quote


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False)
    class Meta:
        model = Quote
        fields = ['author', 'text', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all()

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        return tags_list