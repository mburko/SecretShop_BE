from django.urls import path, re_path
from questions import views

app_name = 'questions'

urlpatterns = [
    re_path(r'^questions$', views.QuestionsEditAPIView.as_view()),
    re_path(r'questions/([0-9]+)', views.QuestionsEditByIdAPIView.as_view()),
    re_path(r'^tags$', views.TagsEditAPIView.as_view()),
    re_path(r'tags/([0-9]+)', views.TagsEditByIdAPIView.as_view()),
    re_path(r'^question_react$', views.QuestionReactionView.as_view())
]
