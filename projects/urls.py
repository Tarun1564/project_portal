from django.urls import path
from . import views

urlpatterns = [
path('coordinator/', views.coordinator_dashboard, name='coordinator_dashboard'),
path('student/', views.student_dashboard, name='student_dashboard'),
path('student/batches/upload-excel/', views.upload_batches_excel, name='upload_batches_excel'),
path("projects/upload-project/<int:batch_id>/", views.upload_project_batch, name="upload_project_batch"),
path("ajax/get-courses/<int:graduation_id>/", views.get_courses, name="get_courses"),
path("ajax/get-branches/<int:graduation_id>/<int:course_id>/",views.get_branches,name="get_branches"),
path("ajax/get-academic-years/<int:branch_id>/", views.get_academic_years, name="get_academic_years"),
path("ajax/get-batches/<int:year_id>/<int:branch_id>/",views.get_batches,name="get_batches"),
path('download-data/<int:year_id>/<int:branch_id>/', views.download_data, name='download_data'),
path('edit-files/<int:project_id>/', views.edit_project_files, name='edit_project_files'),
path('batch/<int:batch_id>/students/', views.batch_students, name='batch_students'),
path('coordinator/approve_project/<int:project_id>/', views.approve_project, name='approve_project'),
path('coordinator/reject_project/<int:project_id>/', views.reject_project, name='reject_project'),
path('download_data/<int:project_id>/', views.download_data, name='download_data'),
path('feedback_view/<int:year_id>/<uuid:feedback_uuid>/', views.guide_feedback, name='guide_feedback'),
path("feedback/submit/<int:project_id>/",views.upload_feedback,name="submit_feedback"),
path("feedback/get_feedback/",views.get_project_paper,name="get_feedback"),
path("feedback/generate/<int:year_id>/<int:branch_id>/",views.generate_feedback_link,name="generate_feedback"),
path("ajax/get_feedback/<int:project_id>/",views.get_feedback_details,name="ajax_get_feedback"),
path("download/batch-excel/<int:year_id>/<int:branch_id>/",views.download_batch_excel,name="download_batch_excel"),
path("download-nptel/",views.download_all_nptel, name="download_all_nptel"),
]
