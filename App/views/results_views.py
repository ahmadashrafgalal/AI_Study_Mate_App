from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from ..models import Student, SummaryCard, Summary, Exam, Question,ExamResult
import requests
import json
import re


@login_required
def results_view(request):
    student = Student.objects.get(user=request.user)
    results = ExamResult.objects.filter(student=student).order_by('-date_taken')

    total_quizzes = results.count()
    total_score = sum(res.score for res in results)
    average_score = total_score / total_quizzes if total_quizzes > 0 else 0
    best_score = max((res.score for res in results), default=0)

    for res in results:
        res.exam_questions = res.exam.questions.count()
        res.exam_questions_answered = int(res.score * int(res.exam_questions) / 100)
        res.questions = f"{res.exam_questions_answered} / {res.exam_questions}"
        print(res.questions)

    context = {
        'results': results,
        'total_quizzes': total_quizzes,
        'average_score': round(average_score, 2),
        'best_score': best_score
    }

    return render(request, 'results_view.html', context)



@login_required
def review_answers(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student = get_object_or_404(Student, user=request.user)
    result = get_object_or_404(ExamResult, exam=exam, student=student)
    questions = Question.objects.filter(exam=exam)

    result.exam_questions = result.exam.questions.count()
    result.exam_questions_answered = int(result.score * int(result.exam_questions) / 100)
    result.questions = f"{result.exam_questions_answered} / {result.exam_questions}"
    print(result.questions)
    
    idx = 0
    for question in questions:
        question.user_answer = result.result.get(str(idx), None)
        idx += 1
        

    context = {
        'result': result,
        'student': student,
        'result': result,
        'questions': questions,
    }

    return render(request, 'review_answers.html', context)