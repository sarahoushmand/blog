from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, filters
from rest_framework.generics import ListAPIView

from datetime import datetime
from django.db.models import Q
from django.http import Http404

from .models import Post, Badge
from .serializers import PostSerializer, BadgeSerializer


class BadgeList(APIView):
    def get(self, request, format=None):
        query = request.query_params.get('query', None)
        if query:
            badges = Badge.objects.filter(name__icontains=query)
        else:
            badges = Badge.objects.all()
        serializer = BadgeSerializer(badges, many=True)
        return Response(serializer.data)


class PostAPIView(APIView):
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer_context = {'user': request.user}
        serializer = self.serializer_class(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            blog_post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

        blog_post.delete()
        message = {'Message': 'Post deleted successfully'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)


class ReleasedPostList(ListAPIView):
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'username']
    ordering_fields = ['title', 'release_date']

    def get_queryset(self):
        current_datetime = datetime.now()
        queryset = Post.objects.filter(state=Post.State.RELEASE, release_date__lte=current_datetime)

        author_username = self.request.query_params.get('username', None)
        if author_username:
            queryset = queryset.filter(author__username__icontains=author_username)

        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(Q(title__icontains=title) | Q(content__icontains=title))

        badges = self.request.query_params.getlist('badges', [])
        if badges:
            badge_ids = [badge.id for badge in Badge.objects.filter(name__in=badges)]
            queryset = queryset.filter(badges__id__in=badge_ids)

        release_date = self.request.query_params.get('release_date', None)
        if release_date:
            queryset = queryset.order_by(release_date)

        return queryset
