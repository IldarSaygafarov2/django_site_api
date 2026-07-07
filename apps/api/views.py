from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from apps.main.models import Category, FAQ, Post, PostComment
from .serializers import (
    CategorySerializer,
    CategoryCreateSerializer,
    FAQSerializer,
    FAQCreateSerializer,
    CategoryUpdateSerializer,
    PostSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
    PostCommentCreateSerializer,
    PostCommentSerializer,
    UserRegistrationSerializer,
    UserProfileSerializer
)

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


@extend_schema(responses={200: UserProfileSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_me(request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

@extend_schema(responses={200: UserProfileSerializer})
@api_view(['GET'])
def get_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

@extend_schema(request=UserRegistrationSerializer, responses={201: UserRegistrationSerializer})
@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # user = serializer.save()
    return Response(serializer.data)

# создать сериалайзер для профиля пользователя
# id, username, email, first_name, avatar
# написать маршрут получающий пользователя по его id
# зарегистрировать его в urls.py


# GET, PUT, POST, DELETE, PATCH

# curl http://127.0.0.1:8000/api/categories/

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateSerializer
        return CategorySerializer  # GET

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new = serializer.save()
        new_serializer = CategorySerializer(new)
        return Response(new_serializer.data)

    @extend_schema(summary='create_new_category',
                   responses={200: CategorySerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_url_kwarg = 'category_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategorySerializer
        return CategoryUpdateSerializer

    @extend_schema(responses={200: CategorySerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request)


@api_view(['GET', 'POST'])
def get_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)

    # request.data
    serializer = CategoryCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    new_category = serializer.save()  # Category
    new_category_serializer = CategorySerializer(new_category)

    return Response(new_category_serializer.data)


@api_view(['GET', 'PATCH', 'DELETE'])
def get_update_delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "GET":
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)

    if request.method == "PATCH":
        serializer = CategoryUpdateSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = serializer.save()
        updated_serializer = CategorySerializer(updated, many=False)
        return Response(updated_serializer.data)

    category.delete()
    return Response({'message': 'Category deleted'})


@api_view(['GET', 'POST'])
def get_or_create_faqs(request):
    if request.method == 'POST':
        serializer = FAQCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        faq = serializer.save()
        faq_serializer = FAQSerializer(faq)
        return Response(faq_serializer.data)

    faqs = FAQ.objects.all()
    data = FAQSerializer(faqs, many=True).data
    return Response(data)


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    # serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    @extend_schema(responses={201: PostDetailSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_post = serializer.save()
        new_post_serializer = PostDetailSerializer(new_post)
        return Response(new_post_serializer.data)
        # return super().post(request)


# class PostCommentCreateView(generics.CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCommentCreateSerializer
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#
#
@extend_schema(request=PostCommentCreateSerializer,
               responses={201: PostCommentSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post_com_serializer = PostCommentCreateSerializer(data=request.data,
                                                      context={'user': request.user,
                                                               'post': post})
    post_com_serializer.is_valid(raise_exception=True)
    com = post_com_serializer.save()
    return Response(PostCommentSerializer(com).data)

# http://127.0.0.1:8000/api/posts/


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        if self.request.method == 'PUT':
            return PostCreateSerializer
        if self.request.method == 'PATCH':
            return PostCreateSerializer



