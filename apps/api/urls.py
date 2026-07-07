from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path('categories/', views.get_categories),  # function based view
    path('categories/', views.CategoryListCreateView.as_view()),
    # path('categories/<int:category_id>/', views.get_update_delete_category),
    path('categories/<int:category_id>/', views.CategoryRetrieveUpdateDestroyView.as_view()),
    path('faqs/', views.get_or_create_faqs),

    path('posts/', views.PostListView.as_view()),
    path('posts/<int:pk>/', views.PostDetailView.as_view()),
    path('posts/<int:pk>/like/', views.add_like),
    path('posts/<int:pk>/dislike/', views.add_dislike),
    path('posts/<int:post_id>/comments/create/', views.create_post_comment),

    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/login/refresh/', TokenRefreshView.as_view()),
    path('auth/register/', views.register_user),
    path('users/me/', views.get_user_me),
    path('users/<int:user_id>/', views.get_user_profile),
]

# i80cvovgc+p07
