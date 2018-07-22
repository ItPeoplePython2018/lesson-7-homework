import math
import random

from bs4 import BeautifulSoup
from django.db.models import Q
from django.test import TestCase

from homework.app.models import Page, Category


class HomeworkTest(TestCase):
    def test_homepage(self):
        # Главная страница (`/`)
        #
        # Должна в отдавать информацию об экземпляре модели `Page` с `id` равным 1:
        #   В заголовке страницы (`title`) название страницы
        #   В теле страницы (`body`) текст страницы
        page = Page.objects.create(id=1, title='Homepage', text='Homepage text')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        html = BeautifulSoup(response.content, "html.parser")
        title = html.select_one('title')
        body = html.select_one('body')

        self.assertEqual(title.text, page.title)
        self.assertEqual(body.text, page.text)

    def test_pages(self):
        # Страница со списком `страниц` (`/pages/`)
        #
        # Должна отдавать в теле страницы список (тег `ul` содержащий `li`) названий всех страниц
        # отсортированных по названию в порядке убывания.
        items = list(range(random.randint(15, 20)))
        random.shuffle(items)
        for idx in items:
            Page.objects.create(title=f'Page #{idx}', text=f'Test of page #{idx}')

        pages = Page.objects.order_by('-title')
        response = self.client.get('/pages/')

        self.assertEqual(response.status_code, 200)
        html = BeautifulSoup(response.content, "html.parser")

        ul = html.select_one('ul')
        for li, page in zip(ul.select('li'), pages):
            self.assertEqual(li.text, page.title)

    def test_category(self):
        # Страница категории (`/category/{id}/`)
        #
        # Должна отдавать в заголовке страницы название категории, а в теле
        # список (тег `ul` содержащий `li`) названий всех страниц
        # из категории отсортированных по названию в порядке увеличения.
        items = list(range(random.randint(15, 20)))
        categories = [
            Category.objects.create(title='First'),
            Category.objects.create(title='Second')
        ]
        choices = [None, ] + categories
        random.shuffle(items)
        for idx in items:
            Page.objects.create(title=f'Page #{idx}', text=f'Test of page #{idx}', category=random.choice(choices))

        category = random.choice(categories)
        pages = Page.objects.filter(category=category).order_by('title')
        response = self.client.get(f'/category/{category.id}/')

        self.assertEqual(response.status_code, 200)
        html = BeautifulSoup(response.content, "html.parser")

        title = html.select_one('title')
        self.assertEqual(title.text, category.title)

        ul = html.select_one('ul')
        for li, page in zip(ul.select('li'), pages):
            self.assertEqual(li.text, page.title)

    def test_category_delete(self):
        """
        При удалении категории также должны удаляться все связанные страницы.
        """

        category = Category.objects.create(title='Deleted')
        page1 = Page.objects.create(title='Undeleted', text='Text')
        page2 = Page.objects.create(title='Deleted #1', text='Text', category=category)
        page3 = Page.objects.create(title='Deleted #2', text='Text', category=category)

        self.assertEqual(Page.objects.count(), 3)
        category.delete()

        self.assertIn(page1, Page.objects.all())
        self.assertNotIn(page2, Page.objects.all())
        self.assertNotIn(page3, Page.objects.all())
        self.assertEqual(Page.objects.count(), 1)

    def test_unknown_category(self):
        # Страница со `страницами` не пренадлежащими не одной категории (`/category/unknown/`)
        #
        # Должна отдавать в теле
        # список (тег `ul` содержащий `li`) названий всех страниц
        # из категории отсортированных по названию в порядке увеличения.
        items = list(range(random.randint(15, 20)))
        categories = [
            Category.objects.create(title='First'),
            Category.objects.create(title='Second')
        ]
        choices = [None, ] + categories
        random.shuffle(items)
        for idx in items:
            Page.objects.create(title=f'Page #{idx}', text=f'Test of page #{idx}', category=random.choice(choices))

        pages = Page.objects.filter(category__isnull=True).order_by('title')
        response = self.client.get(f'/category/unknown/')

        self.assertEqual(response.status_code, 200)
        html = BeautifulSoup(response.content, "html.parser")

        ul = html.select_one('ul')
        for li, page in zip(ul.select('li'), pages):
            self.assertEqual(li.text, page.title)

    def test_category_popularity(self):
        """
        Написать функцию делающую запрос к БД и возвращающую идентификаторы категорий
        чья популярность больше `max_pop` или меньше `min_pop`.
        """

        def get_queryset_result(min_pop, max_pop):
            pass

        popularity_list = [random.randint(0, 100) for _ in range(random.randint(40, 50))]
        categories = []
        for idx, popularity in enumerate(popularity_list):
            categories.append(Category.objects.create(title=f'Category {idx}', popularity=popularity))

        popularity_list.sort()
        center = math.floor(len(popularity_list) / 2)
        length = math.floor(center / 2)
        min_v = center - random.randint(length, center - 1)
        max_v = center - random.randint(length, center - 1)
        result = list(get_queryset_result(min_v, max_v))

        for category in categories:
            if (category.popularity < min_v) or (max_v < category.popularity):
                self.assertIn(category.id, result)
            else:
                self.assertNotIn(category.id, result)
