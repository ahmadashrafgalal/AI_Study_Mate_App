from django.contrib import admin
from .models import Student, SummaryCard, Summary, Exam, Question,ExamResult

admin.site.register((Student, SummaryCard, Summary, Exam, Question, ExamResult))