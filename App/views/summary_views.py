from django.shortcuts import get_object_or_404, render, redirect
from ..models import SummaryCard, Summary, Exam
from django.contrib.auth.decorators import login_required
import re
import requests

WEBHOOK_URL = ""

@login_required
def upload_view(request):
    existing_cards = SummaryCard.objects.filter(student=request.user.student)
    return render(request, 'upload.html', {'existing_cards': existing_cards})


@login_required
def upload_submit(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES.get('image')
        summary_title = request.POST.get('summary-title')
        upload_type = request.POST.get('upload-type')
        summary_card = None
        if upload_type == 'existing':
            print(request.POST.get('summary-card'))
            summary_card = get_object_or_404(SummaryCard, id=request.POST.get('summary-card'))
        elif upload_type == 'new':
            new_card_title = request.POST.get('new-card-title')
            new_card_description = request.POST.get('new-card-description')
            summary_card = SummaryCard.objects.create(
                student=request.user.student,
                title=new_card_title,
                description=new_card_description
            )

        summary = Summary.objects.create(
            img=img,
            title=summary_title,
            summary="temp",
            summary_card=summary_card,
        )

        img.file.seek(0) 
        files = {
            'file': (img.name, img.file.read(), img.content_type)
        }
        try:
            print("Sending image to webhook...")
            response = requests.post(WEBHOOK_URL, files=files)
            print("Image sent successfully.")
            print("Response status code:", response.status_code)
            print("Response content:", response.content)
            if response.status_code == 200:
                data = response.json()
                summary.summary = data.get('output', 'No summary returned.')
                summary.save()
        except Exception as e:
            print(f"Error sending image: {e}")

        return redirect('summary_view', summary_card_id=summary_card.id)
    return render(request, 'upload.html')
    

@login_required
def summary_view(request,summary_card_id):
    summary_card = SummaryCard.objects.get(id=summary_card_id)
    summaries = Summary.objects.filter(summary_card=summary_card)
    for summary in summaries:
        summary.summary = re.sub(r"```html|```", "", summary.summary).strip()
        summary.summary = summary.summary.replace('\\\\n', '').replace('\\\\\\', '').replace('\\', '')
        summary.is_has_exam = Exam.objects.filter(summary=summary).exists()

    return render(request, 'summary.html',{"summary_card": summary_card,"summaries":summaries})

