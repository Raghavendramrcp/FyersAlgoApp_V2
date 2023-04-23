from django.urls import path
from .views import HomePageView, AccessTokenView, delete_auth_code

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('access-token/<int:pk>/',  AccessTokenView.as_view(), name='access_token'),
    path('delete-auth_code/<int:pk>/', delete_auth_code, name='delete_auth_code')
]
