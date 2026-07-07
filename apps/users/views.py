from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from apps.main.models import Post, PostLike, PostDislike
from .forms import RegistrationForm, LoginForm, EditProfileForm
from .models import UserProfile
from apps.tg_bot.models import TelegramBotUser
from apps.tg_bot.bot import bot


def edit_profile_page(request):
    if request.method == 'POST':
        form = EditProfileForm(instance=request.user, data=request.POST)  # instance = элемент который должен обновляться
        if form.is_valid():
            form.save()

            profile_image = request.FILES.get('profile_image')

            if profile_image:  # если была отправлена фотография, то мы ее обновляем в профиле
                request.user.profile.image = profile_image
                request.user.profile.save()
            return redirect('user-profile')

    else:
        form = EditProfileForm()

    context = {
        'form': form
    }
    return render(request, 'users/edit_profile.html', context)


def show_register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():  # проверка на правильность заполненных данных
            user = form.save()  # сохраняет данные из формы в базу данных
            UserProfile.objects.create(
                user=user,
                image=request.FILES.get('profile_image')
            )

            return redirect(f'/tg-bot/confirmation/?user_id={user.id}')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


def show_login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home-page')

    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home-page')


def show_profile_page(request):
    posts = Post.objects.filter(author=request.user)

    for post in posts:
        try:
            post.likes  # проверяем есть ли лайки у поста
        except Exception as e:
            PostLike.objects.create(post=post)

        try:
            post.dislikes
        except Exception as e:
            PostDislike.objects.create(post=post)

    total_posts_views = [post.views_quantity for post in posts]
    user_posts_comments = [post.comments.count() for post in posts]

    # общее кол-во лайков на статьях пользователя
    total_likes = [post.likes.user.count() for post in posts]  # [2,2,2]
    total_dislikes = [post.dislikes.user.count() for post in posts]  # [2,2,2]

    subscribers_total = request.user.profile.subscribers.subscriber.count()
    context = {
        'total_posts': posts.count(),  # select count(id) from posts where author = 1
        'total_posts_views': sum(total_posts_views),
        'total_posts_comments': sum(user_posts_comments),
        'posts': posts,
        'total_likes': sum(total_likes),
        'total_dislikes': sum(total_dislikes),
        'subscribers_total': subscribers_total
    }
    return render(request, 'users/profile.html', context)


from .models import Subscriber
def show_subscribers_page(request):

    current_user = request.user

    subscribers = Subscriber.objects.all()  # [Subscriber, ]

    following_users = []
    for sub in subscribers:
        if current_user in sub.subscriber.all():
            following_users.append(sub)

    following_users = [sub.user_profile.user for sub in following_users]

    context = {
        'following_users': following_users
    }

    return render(request, 'users/subscribers.html', context)

from django.contrib.auth.models import User
from django.http import JsonResponse


def _get_user_profile_and_add_subscriber(user_id):
    user_to_follow = User.objects.get(id=user_id)  # получаем пользователя, на которого хотим подписаться
    user_to_follow_profile, created = UserProfile.objects.get_or_create(user=user_to_follow)

    # добавляем id пользователя, который хочет подписаться в список id подписанных пользователей
    try:
        user_to_follow_profile.subscribers  # post.likes
    except Exception as e:
        Subscriber.objects.create(user_profile=user_to_follow_profile)
    return user_to_follow_profile

def follow_user(request, user_id):
    current_user = request.user  # пользователь, который хочет подписаться
    user_to_follow_profile = _get_user_profile_and_add_subscriber(user_id)

    tg_user = TelegramBotUser.objects.get(user=user_to_follow_profile.user)
    bot.send_message(tg_user.tg_chat_id, f'Пользователь: {current_user.username} подписался на вас')


    user_to_follow_profile.subscribers.subscriber.add(current_user.id)
    return JsonResponse({
        'success': True,
        'message': f'Вы успешно подписались на пользователя: {user_to_follow_profile.user.username}'
    })


def unfollow_user(request, user_id):
    current_user = request.user  # пользователь, который хочет подписаться
    user_to_follow_profile = _get_user_profile_and_add_subscriber(user_id)

    tg_user = TelegramBotUser.objects.get(user=user_to_follow_profile.user)
    bot.send_message(tg_user.tg_chat_id, f'Пользователь: {current_user.username} отписался от вас')

    user_to_follow_profile.subscribers.subscriber.remove(current_user.id)
    return JsonResponse({
        'success': True,
        'message': f'Вы успешно отписались от пользователя: {user_to_follow_profile.user.username}'
    })
# TODO: написать функцию unfollow_user
# сделать все также, как делали для функции follow_user


# TODO: попытаться реализовать функциональность подписки на пользователя и отписки
# follow_user(request, user_id)
# unfollow_user(request, user_id)
# users/<int:user_id>/follow/
# users/<int:user_id>/unfollow/
