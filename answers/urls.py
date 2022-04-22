from django.urls import path, re_path
from answers import views

app_name = 'answers'

urlpatterns = [
    re_path(r'^answers$', views.AnswersEditAPIView.as_view()),
    re_path(r'answers/([0-9]+)', views.AnswersEditByIdAPIView.as_view())
]
