from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post

User = get_user_model()
PAGINATOR_PAGES = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, PAGINATOR_PAGES)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()
    paginator = Paginator(posts, PAGINATOR_PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page})


def profile(request, username):
    if username is None:
        return redirect('index')
    author = get_object_or_404(User, username=username)
    count_post = Post.objects.filter(author=author).count()
    post_list = Post.objects.filter(author=author)
    paginator = Paginator(post_list, PAGINATOR_PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'profile.html',
        {'author': author, 'page': page, 'count': count_post})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = Post.objects.select_related('author').get(id=post_id)
    count_post = Post.objects.filter(author__username=username).count()
    return render(request, 'post.html', {
        'post': post,
        'count': count_post,
        'author': author,
        })


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'new.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('index')


@login_required
def edit_post(request, username, post_id):
    post_edit = Post.objects.get(pk=post_id, author__username=username)
    form = PostForm(request.POST or None, instance=post_edit)
    if post_edit.author.id != request.user.id:
        return redirect('post', username, post_edit.pk)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post', username, post_edit.pk)
    return render(request, 'new.html', {'form': form, 'post_edit': post_edit})
