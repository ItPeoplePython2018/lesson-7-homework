from django.db import models


class Category(models.Model):
    """
    Модель 'Категория':

    title      - название категории
    popularity - популярность категории, измеряется в положительных целых числах, по умолчанию 0
    """
    pass


class Page(models.Model):
    """
    Модель 'Страница':

    title    - название страницы
    text     - тест страницы
    category - необязательная категория (при удалении категории должны удалятся все её страницы)
    """
    pass
