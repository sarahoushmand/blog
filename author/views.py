from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView

from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils import timezone

from .models import AuthorProfile
from post.models import Post, Badge
from .serializers import AuthorProfileSerializer, UserSerializer


class AuthorProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_author_profile(self, user_id):
        try:
            return AuthorProfile.objects.get(user=user_id)
        except AuthorProfile.DoesNotExist:
            return None

    def put(self, request):
        author_profile = self.get_author_profile(request.user.id)
        if author_profile is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorProfileSerializer(author_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        badges = self.request.GET.getlist('badges', [])
        username = self.request.GET.get('username', '')
        count = self.request.GET.get('count', 0)
        release_date_threshold = timezone.now()

        authors = User.objects.annotate(post_count=Count('post')).filter(post_count__gte=count)

        posts = Post.objects.filter(state=Post.State.RELEASE, release_date__lte=release_date_threshold)

        if username:
            authors = authors.filter(Q(username__icontains=username))

        if badges:
            badge_ids = [badge.id for badge in Badge.objects.filter(name__in=badges)]
            posts = posts.filter(badges__id__in=badge_ids)

        authors = authors.filter(post__in=posts).distinct()

        return authors
