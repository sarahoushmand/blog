from django.urls import path
from .views import PostAPIView, BadgeList, ReleasedPostList

urlpatterns = [
    path('create/', PostAPIView.as_view(), name='post-create'),
    path('', ReleasedPostList.as_view(), name='post-list'),
    path('<int:pk>/', PostAPIView.as_view(), name='post-detail'),
    path('badges/', BadgeList.as_view(), name='badge-list'),
]
