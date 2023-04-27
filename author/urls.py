from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import AuthorProfileView, AuthorListView

urlpatterns = [
    path('get-token/', obtain_auth_token, name='get-token'),
    path('update-profile/', AuthorProfileView.as_view(), name='update-profile'),
    path('', AuthorListView.as_view(), name='author-list'),
]
