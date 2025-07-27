from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('home', views.home_view, name='home'),
    path('upload', views.upload_view, name='upload_view'),
    path('summary/<int:summary_card_id>', views.summary_view, name='summary_view'),
    path('exam/<int:exam_id>', views.exam_view, name='exam_view'),
    path('upload/submit', views.upload_submit, name='upload_submit'),
    path('generate_exam/<int:summary_id>', views.generate_exam_view, name='generate_exam_view'),
    path('submit_exam/<int:exam_id>', views.submit_exam_view, name='submit_exam_view'),
    path('results', views.results_view , name="results_view"),
    path('review_answers/<int:exam_id>', views.review_answers, name="results_view_exam"),
    path('share/<uuid:share_token>', views.share_summary_view, name='share_summary_view'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
