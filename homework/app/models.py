from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)   #название категории
    popularity = models.FloatField(default=0)  #популярность категории, измеряется в положительных целых числах, по умолчанию 0
    
    def __str__(self):
        return f'{self.title}::{self.popularity}'

class Page(models.Model):
    title = models.CharField(max_length=100)   #название страницы
    text = models.CharField(max_length=100)    #тест страницы
    category = models.ForeignKey(Category, null=True, related_name='pages', on_delete= models.CASCADE) # категория
    
    def __str__(self):
        return f'{self.title}::{self.text}[{self.category}]'
