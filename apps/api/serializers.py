from rest_framework_simplejwt.tokens import Token

from apps.main.models import Category, FAQ, Post, PostImage, PostComment, PostLike, PostDislike
from django.contrib.auth.models import User
from apps.users.models import UserProfile

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from slugify import slugify

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'password2']

    # serializer.is_valid(raise_exception=True)
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({'password': 'Пароли не совпадают'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)

        token['user_info'] = {
            'id': user.id,
            'username': user.username,
            'is_superuser': user.is_superuser
        }
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField()  # int
#     name = serializers.CharField()  # str
#     slug = serializers.SlugField()  # slug
#     is_active = serializers.BooleanField()
#     created_at = serializers.DateTimeField()  # datetime
#     updated_at = serializers.DateTimeField()  # datetime
#
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'slug', 'is_active', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'is_active', 'created_at', 'updated_at']


class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        model = Category
        fields = ['name']

    def create(self, validated_data):
        print(validated_data)
        slug = slugify(validated_data.get('name'))
        return Category.objects.create(**validated_data, slug=slug)  # name=value


class CategoryUpdateSerializer(serializers.Serializer):
    name = serializers.CharField()
    is_active = serializers.BooleanField()

    class Meta:
        model = Category
        fields = ['name', 'is_active']

    def update(self, instance, validated_data):
        if name := validated_data.get('name'):
            slug = slugify(name)
            validated_data.update({'slug': slug})

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class FAQSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField()
    answer = serializers.CharField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class FAQCreateSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = serializers.CharField()

    class Meta:
        model = FAQ
        fields = ['question', 'answer']

    def create(self, validated_data):
        return FAQ.objects.create(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'short_description', 'preview']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image']


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PostComment
        fields = ['id', 'content', 'user']


class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = UserSerializer()

    comments = PostCommentSerializer(many=True)
    images = PostImageSerializer(many=True)

    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'full_description', 'views_quantity', 'category', 'author', 'comments',
                  'images', 'likes', 'dislikes', 'total_comments']

    def get_total_comments(self, instance):
        return instance.comments.count()

    def get_likes(self, instance):
        total_likes = instance.likes.user.count()
        return total_likes

    def get_dislikes(self, instance):
        total_dislikes = instance.dislikes.user.count()
        return total_dislikes


class PostCreateSerializer(serializers.ModelSerializer):
    preview = serializers.FileField()

    class Meta:
        model = Post
        fields = ['title', 'short_description', 'full_description', 'preview', 'category']

    def create(self, validated_data):
        user = self.context.get('user')

        if not user.is_authenticated:
            raise ValidationError({'message': 'Not authenticated'})

        slug = slugify(validated_data.get('title'))

        if Post.objects.filter(slug=slug).exists():
            raise ValidationError({'message': 'slug not unique'})

        post = Post.objects.create(**validated_data, slug=slug, author=user)

        try:
            post.likes  # проверяем есть ли лайки у поста
        except Exception as e:
            PostLike.objects.create(post=post)

        try:
            post.dislikes
        except Exception as e:
            PostDislike.objects.create(post=post)

        return post


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['content']

    def create(self, validated_data):
        user = self.context.get('user')
        post = self.context.get('post')

        return PostComment.objects.create(user=user, post=post, **validated_data)


# JWT - json web token
# refresh

# djangorestframework-simplejwt

class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'date_joined', 'image']

    def get_image(self, instance):
        image = instance.profile.image
        print(image)
        if not image:
            return None
        return image.url
