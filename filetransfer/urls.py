from django.urls import path
from . import views

urlpatterns = [
	path('upload/', views.FileUploadView.as_view(), name='file-upload'),
	path('download/', views.PersonCSVExportView.as_view(), name='file-download'),
	path('changestatus/', views.ChangeExecutionStatus.as_view(), name='change-status'),
]