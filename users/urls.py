from django.urls import path, re_path

from users.views import RegistrationAPIView, LoginAPIView, UserAPIView, LogOutAPIView,\
    UserProfileView, UserAPIGetByIdView

app_name = 'users'

urlpatterns = [
    path(r'register', RegistrationAPIView.as_view()),
    path(r'login', LoginAPIView.as_view()),
    re_path(r'^users$', UserAPIView.as_view()),
    re_path(r'users/([0-9]+)', UserAPIGetByIdView.as_view()),
    path(r'profile/', UserProfileView.as_view()),
    path(r'logout', LogOutAPIView.as_view())
]
