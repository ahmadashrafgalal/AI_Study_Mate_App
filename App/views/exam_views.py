from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from ..models import Student, SummaryCard, Summary, Exam, Question,ExamResult
import requests
import json
import re


WEBHOOK_URL = ""


@login_required
def exam_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    questions = exam.questions.all()

    formatted_questions = []
    for q in questions:
        formatted_questions.append({
            "question": q.question_text,
            "options": [q.option_1, q.option_2, q.option_3, q.option_4],
        })

    context = {
        "questions_json": json.dumps(formatted_questions),
        "exam": exam,
    }

    return render(request, 'exam.html', context)


@login_required
def generate_exam_view(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id)

    # check if student generate a exam for this summary or not if yes redirect to results_view  
    if Exam.objects.filter(summary=summary, summary__summary_card__student__user=request.user).exists():
        return redirect('results_view')
    

    if request.method == 'POST':

        exam_name = request.POST.get('exam_name', 'Auto Quiz')

        summary = Summary.objects.get(id=summary_id)
        summary.summary = re.sub(r"```html|```", "", summary.summary).strip()
        summary.summary = summary.summary.replace('\\\\n', '').replace('\\\\\\', '').replace('\\', '')
        summary.summary = re.sub(r'<[^>]+>', '', summary.summary).strip()

        response = requests.post(WEBHOOK_URL, data={"summary": summary.summary})
        data = response.json()
        questions_data = data['output']
        questions_data = re.sub(r"```json|```", "", questions_data).strip()
        questions_data = json.loads(questions_data)

        print(questions_data)
        exam = Exam.objects.create(
            summary=summary,
            exam_name=exam_name,
        )

        for q in questions_data:
            print(q)
            Question.objects.create(
                exam=exam,
                question_text=q["question_text"],
                option_1=q["options"][0],
                option_2=q["options"][1],
                option_3=q["options"][2],
                option_4=q["options"][3],
                correct_option=str(q["correct_option"]),
            )

        return redirect('exam_view', exam_id=exam.id)

    return redirect('home')


@login_required
@csrf_exempt
def submit_exam_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student profile not found"}, status=404)

        score = 0
        questions = list(exam.questions.all())
        total = len(questions)

        for index, question in enumerate(questions):
            user_answer = data.get(str(index))
            # print(f"Question {index}: {question.question_text}, User Answer: {user_answer}, Correct Option: {question.correct_option}")
            if user_answer and user_answer == question.correct_option:
                score += 1

        ExamResult.objects.create(
            student=student,
            result=data,
            exam=exam,
            score=(score/total)*100
        )
    return JsonResponse({"redirect_url": reverse('results_view_exam', args=[exam_id])})

