from django.contrib import admin
from django.urls import path
from homework.app.views import start_page, pages_list, categories, pages_with_unknown_category

urlpatterns = [
    path('', start_page),
    path('pages/', pages_list),
    path('category/<int:id>/', categories),
    path('category/unknown/', pages_with_unknown_category),
    path('admin/', admin.site.urls),
]

