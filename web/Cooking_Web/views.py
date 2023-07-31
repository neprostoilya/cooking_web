from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Post, Category, Comment
from django.db.models import F, Q
from .forms import PostAddForm, LoginForm, RegisterForm, CommentForm
from django.contrib.auth import login, logout
from django.contrib import messages

from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import PasswordChangeView


class Index(ListView):
    """Вывод на главную страницу"""

    model = Post
    context_object_name  = 'posts'
    template_name = 'Cooking_web/index.html'
    extra_context = { 
        'title': 'Главная станица'
    }
    def get_queryset(self):
        """Добавление фильтрации"""
        return Post.objects.filter(
            published=True
        )
    
class ArticleByCategory(Index):
    """Реакция на нажатие кнопки категорий"""
    
    def get_queryset(self):
        """Добавление фильтрации"""
        return Post.objects.filter(
            category_id = self.kwargs['pk'],
            published = True
        )
           
    def get_context_data(self, *, objects_list=None, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data()
        category = Category.objects.get(
            pk=self.kwargs['pk']
        )
        context['title'] = category.title
        return context

class PostDetail(DetailView):
    """Страница статьи"""
    model = Post
    template_name = 'Cooking_web/article_detail.html'

    def get_queryset(self):
        """Добавление фильтрации"""
        return Post.objects.filter(
            pk=self.kwargs['pk']
        )

    def get_context_data(self, **kwargs):
        """Для динамических данных"""
        Post.objects.filter(
            pk=self.kwargs['pk']
        ).update(
            watched=F('watched') + 1
        )
        context = super().get_context_data()  
        post = Post.objects.get(
            pk=self.kwargs['pk']
        )
        context['title'] = post.title
        context['comments'] = Comment.objects.filter(post=post)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm

        return context


class PostUpdate(UpdateView): 
    """Кнопка изменения"""
    model = Post
    form_class = PostAddForm
    template_name = 'Cooking_web/article_add_form.html'

class PostDelete(DeleteView):
    """Кнопка удаления"""
    model = Post
    success_url = reverse_lazy('index')
    context_object_name = 'post'

class SearchResult(Index):
    """Кнопка поиска статей"""

    def get_queryset(self):
        """Добавление фильтрации"""
        title = self.request.GET.get('text') 
        posts = Post.objects.filter(
            Q(title__icontains=title) | Q(content__icontains=title)
        )
        return posts
    
def add_comment(request, post_id):
    """Добавление коментариев"""
    form = CommentForm(data=request.POST) 
    if form.is_valid():
        comment = form.save(commit=False)  
        comment.user = request.user 
        post = Post.objects.get(pk=post_id)
        comment.post = post  
        comment.save()  
        messages.success(
            request, 
            message='Ваш комментарий успешно добавлен'
        )
    else:
        pass

    return redirect('article_detail', post_id)

def user_login(request):
    """Аутендификация юзера"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт')
            return redirect('index')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }

    return render(request, 'Cooking_web/login_form.html', context)

class AddPost(CreateView):
    """Добавление статьи от юзера"""
    form_class = PostAddForm
    template_name = 'Cooking_Web/article_add_form.html'
    extra_context = {
        'title': 'Добавить статью'
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')

def register(request):
    """Регистрация юзера"""
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else: 
        form = RegisterForm()
    
    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }
    return render(request, 'Cooking_web/register.html', context)


def profile(request, user_id):
    """Профиль пользователя"""
    user = User.objects.get(
        pk=user_id
    )
    posts = Post.objects.filter(
        author=user
    )
    context = {
        'user': user,
        'posts': posts
    }

    return render(request, 'Cooking_Web/profile.html', context)

class ChangePassword(PasswordChangeView):
    """Cмена пароля"""
    template_name = 'Cooking_Web/password_change_form.html'
    success_url = reverse_lazy('index')