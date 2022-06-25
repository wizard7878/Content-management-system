from django.urls import path, include
from .views import (
    TagApiView, 
    LikeApiView,
    UnLikeApiView, 
    CommentApiViewSet, 
    ContentProfileApiViewSet,
    TopicApiView,
    BookmarkApiViewSet,
    ContentApiViewSet,
    ContentTagFilterApiViewSet,
    ContentTopicFilterApiViewSet
)
from rest_framework.routers import DefaultRouter


comment_router = DefaultRouter()
bookmark_router = DefaultRouter()
all_content_router = DefaultRouter()

profile_content_router = DefaultRouter()
profile_content_router.register('', ContentProfileApiViewSet, basename='content-profile')
comment_router.register('comment', CommentApiViewSet, basename='comment')
bookmark_router.register('bookmark', BookmarkApiViewSet, basename='bookmark')
all_content_router.register('contents', ContentApiViewSet, basename= 'all-content')

urlpatterns = [
    path('tags/', TagApiView.as_view(), name='tag'),
    path('topics/', TopicApiView.as_view(), name='topic'),
    
    path('tag/<str:title>/',ContentTagFilterApiViewSet.as_view({'get': 'list'}), name='content-tag'),
    path('topic/<str:title>/', ContentTopicFilterApiViewSet.as_view({'get': 'list'}), name='content-topic'),
    
    path('like/content/<int:pk>/', LikeApiView.as_view(), name='like'),
    path('unlike/content/<int:pk>/', UnLikeApiView.as_view(), name='unlike'),
    
    path('<int:user_id>/content/', include(profile_content_router.urls)),
    path('', include(all_content_router.urls)),
    path('', include(bookmark_router.urls)),
    path('<int:content_id>/', include(comment_router.urls))
    

    
]