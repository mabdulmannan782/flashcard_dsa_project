from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.subject.name} - {self.name}"
    
class Question(models.Model):
    # subject = models.ForeignKey(Subject, related_name='questions', on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField()  # 1, 2, 3, or 4

class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    answers = models.JSONField()# {question_id: selected_option}
    submitted = models.BooleanField(default=False)