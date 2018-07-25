from django.shortcuts import render
from homework.app.models import Category, Page
from django.db.models import Q


def show_page(request, id=1):
    page = Page.objects.get(id=id)
    return render(request, 'page.html', {
        'page_title': page.title,
        'text': page.text,
    })


def show_pages(request):
    titles = Page.objects.values('title').order_by('-title')
    page_title = 'Pages'
    return render(request, 'pages.html', {
        'page_title': page_title,
        'titles': titles,
    })


def show_category(request, id):
    category = Category.objects.get(id=id)
    category_title = category.title
    category_pages = category.pages.order_by('title')
    return render(request, 'category.html', {
        'page_title': category_title,
        'category_pages': category_pages,
    })


def show_unknown_category(request):
    pages = Page.objects.filter(category__isnull=True).order_by('title')
    page_title = 'unknown category'
    return render(request, 'unknown_category.html', {
        'page_title': page_title,
        'pages': pages,
    })


def get_queryset_result(min_pop, max_pop):
    category_ids_between_max_and_min = Category.objects.values('id').filter(Q(popularity__gt=max_pop)
                                                                            | Q(popularity__lt=min_pop))
    return [item['id'] for item in category_ids_between_max_and_min]
