from django.contrib import admin
from .models import HomeSlider, Category, Post, PostComment, PostImage, FAQ

# файл для регистрации наших таблиц в админ панели


class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']  # поля таблицы, которые будут показаны на странице всех элементов


# регистрация модели в админ панели
admin.site.register(HomeSlider, HomeSliderAdmin)

# привет мир -> privet-mir


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'is_active', 'created_at']
    list_display_links = ['id', 'name']  # список полей, при нажатии на которые, переходим на детальную страницу
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']  # список полей, которые можно менять на странице всех элементов
    list_filter = ['is_active', 'created_at']  # список полей для фильтрации элементов
    search_fields = ['name']


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


# TODO: сделать отображение фотографий в слайдере


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'views_quantity', 'author', 'category']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_quantity']
    list_filter = ['author', 'category', 'created_at']
    inlines = [PostImageInline]
    list_editable = ['author', 'category']


# добавить по 2 поста на 1 категорию
# отобразить посты на странице news

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'show_content', 'user', 'post', 'created_at']
    list_filter = ['user', 'post', 'created_at']
    search_fields = ['content']

    @admin.display(description='Комментарий')
    def show_content(self, obj):
        return obj.content[:60]



@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass

