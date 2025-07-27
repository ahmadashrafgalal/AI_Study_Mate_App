from django.shortcuts import render
from ..models import SummaryCard
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    summary_cards = SummaryCard.objects.filter(student=request.user.student)
    return render(request, 'index.html', {'summary_cards': summary_cards})
