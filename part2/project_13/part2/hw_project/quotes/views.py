from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AuthorForm, QuoteForm
from .models import Quote, Author, Tag


def main(request, page=1):
    quotes = Quote.objects.select_related('author').prefetch_related('tags').all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    # Запит до бази даних, щоб підрахувати кількість цитат для кожного тега
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]


    return render(request, 'quotes/index.html',
                  context={'quotes': quotes_on_page, 'paginator': paginator, 'top_tags': top_tags})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def add_author(request):
    if not request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:add_quote')
        else:
            return render(request, 'quotes/add_author.html', {'form': form})
    return render(request, 'quotes/add_author.html', {'form': AuthorForm()})


@login_required
def add_quote(request):
    if not request.user.is_authenticated:
        return redirect(to='quotes:root')

    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)  # Встановлюємо commit=False, щоб не зберігати дані до бази даних наразі
            new_quote.author_id = request.POST.get(
                'author')  # Встановлюємо автора за допомогою ідентифікатора, вибраного з форми
            new_quote.save()

            # choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))

            tags_selected = request.POST.getlist('tags')
            print("Tags selected:", tags_selected)

            choice_tags = Tag.objects.filter(id__in=tags_selected)
            print("Choice tags:", choice_tags)

            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect('/')
        else:
            return render(request, 'quotes/add_quote.html', {'form': form})

    return render(request, 'quotes/add_quote.html', {'tags': tags, 'authors': authors})


def quotes_by_tag(request, tag_id, page=1):
    tag = Tag.objects.get(pk=tag_id)
    quotes = Quote.objects.filter(tags=tag)

    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    # Запит до бази даних, щоб підрахувати кількість цитат для кожного тега
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]

    return render(request, 'quotes/quotes_by_tag.html',
                  {'tag': tag, 'quotes': quotes_on_page, 'paginator': paginator, 'top_tags': top_tags})
