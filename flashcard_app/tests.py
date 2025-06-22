from django.test import TestCase
from .models import Subject, Question

class SubjectModelTest(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name="Data Structures")

    def test_subject_creation(self):
        self.assertEqual(self.subject.name, "Data Structures")

class QuestionModelTest(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name="Algorithms")
        self.question = Question.objects.create(
            subject=self.subject,
            text="What is the time complexity of binary search?",
            option1="O(n)",
            option2="O(log n)",
            option3="O(n log n)",
            option4="O(1)",
            correct_option=2
        )

    def test_question_creation(self):
        self.assertEqual(self.question.text, "What is the time complexity of binary search?")
        self.assertEqual(self.question.correct_option, 2)

    def test_question_options(self):
        self.assertIn("O(log n)", [self.question.option1, self.question.option2, self.question.option3, self.question.option4])