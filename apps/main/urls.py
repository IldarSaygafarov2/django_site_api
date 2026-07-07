from django.urls import path

from . import views

# список ссылок для приложения main

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/about/

urlpatterns = [
    path('', views.render_home_page, name='home-page'),
    path('about/', views.show_about_page, name='about-page'),
    path('faq/', views.show_faq_page, name='faq-page'),
    path('news/', views.show_news_page, name='news-page'),
    path('news/categories/<slug:category_slug>/', views.show_news_by_category,
         name='news-category-page'),
    path('news/create/', views.create_post, name='create-post'),
    path('news/search/', views.search_page, name='search-page'),
    path('news/<slug:slug>/', views.show_post_detail_page, name='news-detail'),
    path('news/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='news-edit'),
    path('news/<slug:slug>/delete/', views.DeletePostView.as_view(), name='news-delete'),
    path('news/<slug:post_slug>/<str:action>/', views.add_like_or_dislike, name='vote')
]

# {% url 'news-detail' post.slug %}
# post.get_absolute_url