from django.test import TestCase
from .models import Questions


# Create your tests here.
class QuestionsTestCase(TestCase):
    def test_something(self):
        self.assertEqual(str(Questions.objects.all().filter(author_id=5)), '<QuerySet []>')
