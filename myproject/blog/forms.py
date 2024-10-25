from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment

# Этот класс наследует от ModelForm, что позволяет автоматически создавать форму на основе модели User.
# Поля формы:
# password и password_confirm: Эти поля создаются как поля ввода пароля с использованием виджета PasswordInput,
# который скрывает вводимые символы.
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    # Указывает, что эта форма связана с моделью User и определяет поля,
    # которые будут включены в форму: username, email и password.
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Этот метод вызывается при валидации формы. Он получает очищенные данные (cleaned_data) и проверяет,
    # совпадают ли введенные пароли. Если они не совпадают, выбрасывается ошибка валидации с сообщением
    # "Пароли не совпадают".
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")

#  Этот класс также наследует от ModelForm, что позволяет создавать форму на основе модели Post.
class PostForm(forms.ModelForm):
    # Meta-класс:
    # Указывает, что эта форма связана с моделью Post и определяет поля, которые будут включены в форму:
    # title и content. Это означает, что пользователь сможет вводить заголовок и содержимое поста через эту форму.
    class Meta:
        model = Post
        fields = ['title', 'content']


# Наследование от forms.ModelForm: Как и предыдущие классы, этот класс наследует от ModelForm,
# позволяя создавать форму на основе модели Comment.
# Meta-класс:
# Указывает, что эта форма связана с моделью Comment и определяет поле, которое будет включено в форму:
# только поле content. Это означает, что пользователь сможет вводить текст комментария через эту форму.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

