from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class PostAddForm(forms.ModelForm):
    """Класс для добавлений статей от юзера"""
    class Meta:
        """Мета класс указывает на поведенческий характер (черчеж класса)"""
        model = Post
        fields = [
            'title',
            'content',
            'photo',
            'category'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class LoginForm(AuthenticationForm):
    """Форма аунтедификации юзера"""
    username = forms.CharField(
        label="Имя",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

class RegisterForm(UserCreationForm):
    """Форма регистрации юзера"""

    class Meta:
        """Мета класс указывает на поведенческий характер (черчеж класса)"""
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Почта'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердить пароль'
        })
    )

class CommentForm(forms.ModelForm):
    """Форма для коментария"""
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст вашего комментария'
            })
        }