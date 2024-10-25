"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import post_list, post_detail, post_create, post_edit, register, user_login, home, add_comment

urlpatterns = [
    path('admin/', admin.site.urls),  # Этот путь указывает на административный интерфейс Django
    path('', home, name='home'),  # URL для главной страницы
    path('post/<int:pk>/', post_detail, name='post_detail'),  # URL, который содержит идентификатор поста
    path('post/new/', post_create, name='post_create'),  # URL для создания нового поста.
    path('post/<int:pk>/edit/', post_edit, name='post_edit'),  # URL для редактирования существующего поста
    path('posts/', post_list, name='post_list'),  # URL для отображения списка всех постов.
    path('register/', register, name='register'),  # URL для регистрации
    path('login/', user_login, name='login'),  # URL для входа
    path('post/<int:pk>/', post_detail, name='post_detail'),  # URL для просмотра поста
    path('post/<int:post_id>/add_comment/', add_comment, name='add_comment'),  # Пример URL для добавления комментария
]
