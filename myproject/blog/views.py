from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, UserRegistrationForm, CommentForm
from .models import Post


# Это функция, которая отвечает за отображение домашней страницы приложения.
def home(request):
    posts = Post.objects.all()  # Получаем все посты
    return render(request, 'blog/home.html', {'posts': posts})


# Эта функция обрабатывает запросы на получение списка всех постов.
# Она извлекает все посты из базы данных с помощью Post.objects.all() и передает их в шаблон post_list.html.
def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)  # Показывать 5 постов на странице

    page_number = request.GET.get('page')  # Получаем номер страницы из GET-запроса
    page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


# Эта функция обрабатывает запросы на получение подробной информации о конкретном посте.
# Она использует get_object_or_404, чтобы получить пост по первичному ключу (pk). Если пост не найден,
# будет возвращена ошибка 404.
# Пост передается в шаблон post_detail.html.
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Пагинация комментариев
    comments = post.comments.all()
    paginator = Paginator(comments, 5)  # Показывать 5 комментариев на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'page_obj': page_obj})


# Это функция, которая добавляет комментарий к посту
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Устанавливаем автора комментария
            comment.save()
            return redirect('post_detail', pk=post_id)  # Перенаправление на страницу поста после добавления комментария

    return redirect('post_detail', pk=post_id)  # Если GET-запрос или форма не валидна


# Эта функция обрабатывает запросы на создание нового поста.Если метод запроса — POST (т.е. форма была отправлена),
# она создает экземпляр формы с данными из запроса и проверяет его на валидность. Если форма валидна,
# данные сохраняются в базе данных, и происходит перенаправление на страницу списка постов.
# Если метод запроса не POST (т.е. пользователь только что открыл страницу), создается пустая форма для ввода данных
# В любом случае форма передается в шаблон post_form.html
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# Эта функция обрабатывает запросы на редактирование существующего поста.
# Если метод запроса — POST, создается экземпляр формы с данными из запроса и текущим объектом (instance=post).
# Если форма валидна, изменения сохраняются в базе данных и происходит перенаправление на страницу подробностей
# этого поста.
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


# Это функция, которая обрабатывает запросы на регистрацию нового пользователя.
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Храните пароль в зашифрованном виде
            user.save()
            login(request, user)  # Вход пользователя после регистрации
            return redirect('post_list')  # Перенаправление на страницу со списком постов
    else:
        form = UserRegistrationForm()

    return render(request, 'blog/register.html', {'form': form})


# Это функция представления, которая принимает объект request в качестве аргумента. Она обрабатывает запросы
# на вход пользователя.
def user_login(request):  #
    if request.method == "POST":  # Если метод запроса — POST, это означает, что пользователь отправил форму для входа.
        form = AuthenticationForm(data=request.POST)  # Создается экземпляр формы AuthenticationForm,
        # и передаются данные из POST-запроса. Эта форма предназначена для аутентификации пользователей.
        if form.is_valid():  # Проверяется, является ли форма валидной (например, заполнены ли все необходимые поля).
            username = form.cleaned_data['username']  # Если форма валидна, извлекаются имя пользователя и
            password = form.cleaned_data['password']  # пароль из очищенных данных формы.
            user = authenticate(username=username, password=password)  # Функция authenticate проверяет,
            # существуют ли указанные имя пользователя и пароль в базе данных. Если аутентификация успешна,
            # возвращается объект пользователя; если нет — None.
            if user is not None:  # Если пользователь успешно аутентифицирован (т.е. user не равен None),
                login(request, user)  # вызывается функция login, которая устанавливает сессию для пользователя.
                return redirect('post_list')
    else:
        form = AuthenticationForm()  # Если метод запроса не POST (т.е. пользователь только что открыл страницу),
        # создается пустая форма для ввода данных.

    return render(request, 'blog/login.html', {'form': form})  # В конце функция возвращает
    # рендеринг шаблона login.html, передавая в него форму (как контекст).


# Это функция представления, которая принимает два аргумента:
# request: объект запроса, который содержит информацию о текущем HTTP-запросе.
# первичный ключ (primarypk:  key) поста, который передается через URL. Он используется для идентификации конкретного
# поста в базе данных.
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
