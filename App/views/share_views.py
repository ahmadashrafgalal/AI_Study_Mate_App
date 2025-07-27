from ..models import Summary, Student
from django.shortcuts import render, get_object_or_404
import re


def share_summary_view(request, share_token):
    summary = get_object_or_404(Summary, share_token=share_token)
    summary.summary = re.sub(r"```html|```", "", summary.summary).strip()
    summary.summary = summary.summary.replace('\\\\n', '').replace('\\\\\\', '').replace('\\', '')

    return render(request, 'share.html', {'summary': summary})