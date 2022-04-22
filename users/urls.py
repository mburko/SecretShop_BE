from django.urls import path, re_path

from users.views import RegistrationAPIView, LoginAPIView, UserAPIView, LogOutAPIView,\
    UserProfileView

app_name = 'users'

urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    re_path(r'^users$', UserAPIView.as_view()),
    re_path(r'users/([0-9]+)', UserAPIView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('logout', LogOutAPIView.as_view())
]
