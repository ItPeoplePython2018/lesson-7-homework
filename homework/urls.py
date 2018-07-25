from django.contrib import admin
from django.urls import path
from homework.app.views import show_page, show_pages, show_category, show_unknown_category


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', show_page),
    path('<int:id>/', show_page),
    path('pages/', show_pages),
    path('category/<int:id>', show_category),
    path('category/unknown', show_unknown_category),
]
