from homework.app.models import Category, Page
from django.shortcuts import render

def start_page(request):
    page = Page.objects.get(id=1)
    return render(request, 'start_page.html', {
        'title': page.title,
        'text': page.text
    })

def pages_list(request):
    pages = Page.objects.order_by('-title')
    return render(request, 'Pages.html', {
        'object_list': pages
    })

def categories(request, id):
    category = Category.objects.get(id=id)
    pages = Page.objects.filter(category=category).order_by('title')
    return render(request, 'category.html', {
        'title': category.title,
        'category_pages': pages
    })

def pages_with_unknown_category(request):
    unknown_pages = Page.objects.filter(category__isnull=True).order_by('title')
    return render(request, 'unknown.html', {
        'unknown_pages': unknown_pages
    })

def get_queryset_result(min_pop, max_pop):
    categories_min = Category.objects.filter(popularity__lt=min_pop)
    categories_max = Category.objects.filter(popularity__gt=max_pop)
    result = []

    for category in categories_min:
        result.append(category.id)
    for category in categories_max:
        result.append(category.id)

    return result
    # так же можно сделать сложный запрос, используя Q


