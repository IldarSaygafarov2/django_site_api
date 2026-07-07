from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse
from apps.tg_bot.bot import bot
from apps.tg_bot.models import TelegramBotUser
from .forms import PostForm
from .models import HomeSlider, Category, Post, PostComment, UserPostView, PostLike, PostDislike, FAQ


class DeletePostView(DeleteView):
    model = Post
    template_name = 'main/post_confirm_delete.html'
    success_url = '/'
    slug_url_kwarg = 'slug'


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'main/news_create.html'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.slug = slugify(form.title)
        form.save()
        return redirect(self.object.get_absolute_url())  # self.object = Пост, который обновляется

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     print(self.request.POST , data['form'].is_valid())
    #     if self.request.PUT and data['form'].is_valid():
    #         print(data['form'].title)
    #     return data


# Create your views here.


# http://127.0.0.1:8000/
# http://127.0.0.1:8000/about/
# hello, world

# select * from main_homeslider;


def render_home_page(request):  # request - это запрос текущей страницы
    slider_photos = HomeSlider.objects.all()  # select * from main_homeslider;

    posts = Post.objects.all()

    most_viewed = posts.order_by('-views_quantity')[:4]
    recently_added = posts.order_by('-created_at')[:4]

    context = {
        'slider_photos': slider_photos,
        'most_viewed': most_viewed,
        'recently_added': recently_added
    }

    return render(request, 'main/index.html', context)


def show_about_page(request):
    return render(request, 'main/about.html')


def show_faq_page(request):
    faqs = FAQ.objects.all()

    context = {
        'faqs': faqs
    }

    return render(request, 'main/faq.html', context)


categories_data = ['Спорт', 'Политика', 'Мир', 'Космос']


def show_news_page(request):
    categories = Category.objects.all()  # select * from main_categories;
    posts = Post.objects.all().order_by('-created_at')  # desc

    # posts - QuerySet - список объектов с базы данных
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)  # получаем посты переданной страницы

    context = {
        'categories_data': categories,
        'posts': posts
    }
    return render(request, 'main/news.html', context)


# http://127.0.0.1:8000/news/categories/10

def show_news_by_category(request, category_slug):
    categories_data = Category.objects.all()

    # можно получить ошибку если: 1) получено больше 1 значения 2) если значение не получено
    category = Category.objects.get(slug=category_slug)  # select * from main_categories where slug = ?

    posts = Post.objects.filter(category=category)
    # .filter()

    context = {
        'categories_data': categories_data,
        'category': category,
        'posts': posts
    }
    return render(request, 'main/news.html', context)


from django.shortcuts import get_object_or_404


def show_post_detail_page(request, slug):
    post = get_object_or_404(Post, slug=slug)

    try:
        post.likes  # проверяем есть ли лайки у поста
    except Exception as e:
        PostLike.objects.create(post=post)

    try:
        post.dislikes
    except Exception as e:
        PostDislike.objects.create(post=post)

    if request.method == 'POST':
        comment = PostComment.objects.create(
            user=request.user,
            post=post,
            content=request.POST['post_comment']
        )
        comment.save()

        post_author_tg = TelegramBotUser.objects.get(user=post.author)

        bot.send_message(
            chat_id=post_author_tg.tg_chat_id,
            text=f'''
На пост: <a href="http://127.0.0.1:8000/news/{post.slug}">{post.title}</a>
Был добавлен комментарий

<i>{comment.content}</i>
''', parse_mode='HTML'
        )
        return redirect('news-detail', slug)

    if request.user.is_authenticated:
        post_view, post_views_created = UserPostView.objects.get_or_create(
            user=request.user,
            post=post
        )
        if post_views_created:
            post.views_quantity += 1
            post.save()

    is_subscribed = request.user in post.author.profile.subscribers.subscriber.all()

    context = {
        'post': post,
        'is_subscribed': is_subscribed
    }

    return render(request, 'main/news_detail.html', context)


# TODO: сделать отображение комментариев поста
# если комментариев у поста нету, написать "Нет комментариев"

from slugify import slugify


def create_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)  # commit=False - не отправяет данные в БД
            form.author = request.user
            form.slug = slugify(form.title)
            form.save()  # сохраняем измененный объект в БД
            return redirect('news-detail', form.slug)
    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'main/news_create.html', context)


# users/me/ - страница профиля пользователя


# add_like
# add_dislike

def add_like_or_dislike(request, post_slug, action):
    post = Post.objects.get(slug=post_slug)

    post_author_tg = TelegramBotUser.objects.get(user=post.author)
    temp = ""
    user = request.user
    user_info = user.first_name or user.username
    if action == 'add_like':
        if user not in post.likes.user.all():  # все пользователи ставившие лайк
            post.likes.user.add(user.id)  # добавляем ID пользователя в таблицу лайков
            post.dislikes.user.remove(user.id)  # Убираем ID пользователя из таблицы дизлайков
            temp = f'На пост {post.title} был добавлен лайк и убран дизлайк от пользователя {user_info}'
        else:
            post.likes.user.remove(user.id)
            temp = f'На пост {post.title} был убран лайк от пользователя {user_info}'
    elif action == 'add_dislike':
        if user not in post.dislikes.user.all():  # все пользователи ставившие лайк
            post.dislikes.user.add(user.id)  # добавляем ID пользователя в таблицу лайков
            post.likes.user.remove(user.id)  # Убираем ID пользователя из таблицы дизлайков
            temp = f'На пост {post.title} был добавлен дизлайк и убран лайк от пользователя {user_info}'
        else:
            post.dislikes.user.remove(user.id)
            temp = f'На пост {post.title} был убран дизлайк от пользователя {user_info}'

    msg = f"""
{temp}

Кол-во лайков и дизлайков:
Лайки: {post.likes.user.count()}
Дизлайки: {post.dislikes.user.count()}
"""
    bot.send_message(post_author_tg.tg_chat_id, msg)
    return redirect('news-detail', post_slug)


from django.db.models import Q


def search_page(request):
    query = request.GET.get('q')

    if not query:
        qs = Post.objects.all()
    else:
        qs = Post.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(full_description__icontains=query)
        )

    context = {
        'posts': qs
    }

    return render(request, 'main/search.html', context)
