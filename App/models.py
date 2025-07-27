from django.contrib.auth.models import User
from django.db import models
import uuid

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_images', default='default.jpg')
    YEAR_CHOICES = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    ]
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    

    def __str__(self):
        return self.user.username

class SummaryCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Summary(models.Model):
    img = models.ImageField(upload_to='summary_images', blank=True, null=True)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    summary_card = models.ForeignKey(SummaryCard, on_delete=models.CASCADE, related_name='summaries')
    created_at = models.DateTimeField(auto_now_add=True)
    share_token = models.UUIDField(default=uuid.uuid4, unique=True)


    def __str__(self):
        return f"Summary for {self.summary_card.title} by {self.summary_card.student.user.username}"
    
class Exam(models.Model):
    exam_name = models.CharField(max_length=200)
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, related_name='exams')

    def __str__(self):
        return f"{self.exam_name} for {self.summary}"


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    CHOICES = [
        ('1', 'Option_1'),
        ('2', 'Option_2'),
        ('3', 'Option_3'),
        ('4', 'Option_4'),
    ]
    correct_option = models.CharField(max_length=1, choices=CHOICES)

    def __str__(self):
        return f"Question: {self.question_text} for Exam: {self.exam.exam_name}"

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    result = models.JSONField()
    score = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"Result: {self.score} for {self.student.user.username} in {self.exam.exam_name}"
    
