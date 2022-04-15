from django.urls import path

from users.views import RegistrationAPIView, LoginAPIView, UserAPIView, LogOutAPIView

app_name = 'users'

urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('logout', LogOutAPIView.as_view())
]
