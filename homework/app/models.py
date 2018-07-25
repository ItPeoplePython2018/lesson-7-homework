from django.db import models


class Category(models.Model):
    """
    Модель 'Категория':

    title      - название категории
    popularity - популярность категории, измеряется в положительных целых числах, по умолчанию 0
    """
    title = models.CharField(max_length=100)
    popularity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Category {self.title}, category's popularity is {self.popularity}"


class Page(models.Model):
    """
    Модель 'Страница':

    title    - название страницы
    text     - тест страницы
    category - необязательная категория (при удалении категории должны удалятся все её страницы)
    """
    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.ForeignKey('Category', null=True, related_name='pages', on_delete=models.CASCADE)

    def __str__(self):
        return f'Page {self.title} related to {self.category}'
