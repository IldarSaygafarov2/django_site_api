import uuid
from django.db import models
from django.urls import reverse

# файл для работы с таблицами базы данных

# created_at
# updated_at


"""
create table if not exists categories(
    id integer primary key autoincrement,
    
);
"""


# ORM

# main_homeslider


class HomeSlider(models.Model):
    id = models.UUIDField(editable=False, primary_key=True,
                          default=uuid.uuid4)
    image = models.ImageField(upload_to='home/slider/',
                              verbose_name='Фото')  # media/home/slider/image_name.png | verbose_name=название_поля_в_админ_панели

    def __str__(self):  # строковое представление класса
        return f'Фотка с ID: {self.id}'

    class Meta:
        verbose_name = 'Фото слайдера'  # название таблицы в единственном числе
        verbose_name_plural = 'Фотки слайдера'  # название таблицы во множественном числе


# абстрактная модель

class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)  # 2026-04-09 15:08:24
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    class Meta:
        abstract = True  # делает так, чтобы эта модель, не добавлялась в БД


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=120, unique=True, verbose_name='Короткая ссылка')
    is_active = models.BooleanField(default=True, verbose_name='Активна?')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(BaseModel):
    title = models.CharField(verbose_name="Название", max_length=120, unique=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=140, unique=True)
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание', null=True, blank=True)
    preview = models.ImageField(upload_to='posts/previews/%Y/%m/%d',
                                verbose_name='Превью')  # media/post/%Y/%m/%d  2026/04/14
    views_quantity = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    is_active = models.BooleanField(verbose_name='Активна ли статья?', default=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def get_absolute_url(self):  # метод для получения ссылки на детальную страницу
        return reverse('news-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


"""
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(id)
"""

"""
создать таблицу PostComment
user
post
content
created_at
updated_at

зарегистрировать ее в админ панели
"""


class PostComment(BaseModel):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='Статья')
    content = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'Комментарий для "{self.post.title}" от "{self.user.username}"'

    class Meta:
        verbose_name = 'Комментарий поста'
        verbose_name_plural = 'Комментарии постов'


def make_post_image_path(instance: "PostImage", filename: str):
    return f'posts/images/{instance.post.slug}/{filename}'


class PostImage(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='images', verbose_name='Пост')
    image = models.ImageField(verbose_name='Фото', upload_to=make_post_image_path)

    class Meta:
        verbose_name = 'Фото поста'
        verbose_name_plural = 'Фото поста'


"""
сделать переход на страницу создания поста

зарегистрировать ссылку до ссылки на детальную страницу
"""


class UserPostView(BaseModel):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             verbose_name='Пользователь')  # admin
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             verbose_name='Пост', related_name='post_views')


class PostLike(BaseModel):
    user = models.ManyToManyField('auth.User', related_name='likes')
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='likes')


class PostDislike(BaseModel):
    user = models.ManyToManyField('auth.User', related_name='dislikes')
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='dislikes')


class FAQ(BaseModel):
    question = models.CharField(max_length=100, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'



# создать таблицу FAQ

# question CharField
# answer TextField

# Зарегистрировать данную модель в админ панели
# добавить 3 записи в эту таблицу
# на странице faq.html вывести вопросы-ответы
