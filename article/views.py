from rest_framework import generics, viewsets, status, filters
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import  (
    TopicSerializer,
    TagSerializer, 
    ContentSerializer, 
    ContentDetailSerializer, 
    CommentSerializer,
    BookmarkSerializer,
    BookMarkListSerializer,
)
from core.models import Bookmark, Like, Tag, Content, Comment, Topic, User
from .permissions import IsAuthor
# Create your views here.

class TagApiView(generics.ListCreateAPIView):
    """
    List tags and filtering them
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)


class TopicApiView(generics.ListAPIView):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


class ContentProfileApiViewSet(viewsets.ModelViewSet):
    """
    Api create list retrieve edit and delete contents
    you only have permission to edit and delete your content
    """
    permission_classes = (IsAuthenticated, IsAuthor,)
    serializer_class = ContentSerializer
    queryset = Content.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            self.serializer_class = ContentDetailSerializer

        return self.serializer_class

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        if user:
            return self.queryset.filter(author= user, publish=True)
        return self.queryset.filter(publish=True)


class ContentApiViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    Api list all contents and filter by serach fields
    """
    
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ('title', 'body')

    def get_queryset(self):
        return self.queryset.filter(publish=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            self.serializer_class = ContentDetailSerializer

        return self.serializer_class


class ContentTagFilterApiViewSet(viewsets.GenericViewSet, ListModelMixin):
    """
    Api list content by tag
    """
    serializer_class = ContentSerializer
    queryset = Content.objects.all()

    def get_queryset(self):
        keyword = self.kwargs['title']
        return self.queryset.filter(tags__title = keyword)


class ContentTopicFilterApiViewSet(viewsets.GenericViewSet, ListModelMixin):
    """
    Api list content by topic
    """
    serializer_class = ContentSerializer
    queryset = Content.objects.all()

    def get_queryset(self):
        keyword = self.kwargs['title']
        topic = Topic.objects.get(title=keyword)
        return self.queryset.filter(topic = topic,publish=True)


class LikeApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk=None):
        content_id = pk
        content = Content.objects.get(id=content_id)
        if Like.objects.get(user=self.request.user, content=content):
            return Response({"message": "You have been liked this content"}, status= status.HTTP_403_FORBIDDEN)
        Like.objects.create(content=content, liked=True, user=self.request.user)
        return Response(ContentDetailSerializer(content).data, status= status.HTTP_200_OK)


class UnLikeApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk=None):
        content_id = pk
        content = Content.objects.get(id=content_id)
        liked_content = Like.objects.get(user=self.request.user, content=content)
        if liked_content:
            liked_content.delete()
            return Response(ContentDetailSerializer(content).data, status= status.HTTP_200_OK)
        return Response({"message": "You have been unliked this content"}, status= status.HTTP_403_FORBIDDEN)


class CommentApiViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        content_id = self.kwargs['content_id']
        content = Content.objects.get(id=content_id)
        return self.queryset.filter(content=content)


class BookmarkApiViewSet(viewsets.GenericViewSet, 
                        ListModelMixin, 
                        CreateModelMixin, 
                        DestroyModelMixin):

    permission_classes = (IsAuthenticated, )
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            self.serializer_class = BookMarkListSerializer
        return self.serializer_class


    
