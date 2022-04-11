from django.urls import path, re_path
from questions import views

app_name = 'questions'

urlpatterns = [
    re_path(r'^questions$', views.QuestionsEditAPIView.as_view()),
    re_path(r'questions/([0-9]+)', views.QuestionsEditByIdAPIView.as_view())
]
