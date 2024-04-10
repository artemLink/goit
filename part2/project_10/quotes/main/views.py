from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Author, Quote
from .forms.form import AuthorForm, QuoteForm
from django.contrib.auth.decorators import login_required
def index(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes.html', {'quotes': quotes})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author_detail.html', {'author': author})


@login_required
def add_new_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()

    return render(request, 'add_author.html', {'form': form})


@login_required
def add_new_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuoteForm()

    return render(request, 'add_quote.html', {'form': form})