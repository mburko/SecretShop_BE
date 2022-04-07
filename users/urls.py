from django.urls import path

from users.views import RegistrationAPIView, LoginAPIView

app_name = 'users'

urlpatterns = [
    path('users/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view())
]
