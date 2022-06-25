from multiprocessing import context
from rest_framework import serializers
from core import models
from django.contrib.auth import get_user_model

from user.serializer import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('title', )

    def create(self, validated_data):
        tag = models.Tag.objects.create(title = validated_data['title'])
        return tag


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ('title', 'image')


class ContentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    likes = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Tag.objects.all()
    )

    class Meta:
        model = models.Content
        fields = ('id', 'title', 'body', 'tags', 'topic', 'author', 'likes', 'publish')
        read_only_fields = ('id',)

    def get_likes(self, obj):
        return models.Like.objects.filter(content=obj).count()
         


class ContentDetailSerializer(ContentSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(many=False, read_only=True)
    topic = TopicSerializer(many=False, read_only=True)
    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return models.Like.objects.filter(content=obj).count()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)

    def validate(self, attrs):
        view = self.context['view']
        content_id = view.kwargs['content_id']
        content = models.Content.objects.get(id=content_id)
        comments_ids = list(models.Comment.objects.filter(content=content).values_list('id', flat=True))

        if attrs.get('reply') is not None:
            if attrs.get('reply').id in comments_ids:
                return super().validate(attrs)
            else:
                raise serializers.ValidationError('There is no comment id in this content')
        return super().validate(attrs)

    class Meta:
        model = models.Comment 
        fields = ('id', 'author', 'reply', 'body')
        read_only_fields = ('id',)
    
    
    def create(self, validated_data):
        view = self.context['view']
        content_id = view.kwargs['content_id']
        return models.Comment.objects.create(
            **validated_data, 
            author=self.context['request'].user, 
            content=models.Content.objects.get(id=content_id)
        )


class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Bookmark
        fields = ('content', 'user' )

    def validate(self, attrs):
        bookmarked = models.Bookmark.objects.filter(content= attrs['content'], user=self.context['request'].user)
        
        if attrs['content'].publish and list(bookmarked) == []:
            return attrs
        raise serializers.ValidationError('NotFound')


class BookMarkListSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=False, read_only=True)

    class Meta:
        model = models.Bookmark
        fields = ('content',)




