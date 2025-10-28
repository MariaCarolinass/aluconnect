from django.urls import path
from apps.progress.views import RegisterProgressView, ProgressListView, CourseProgressView

urlpatterns = [
    path('courses/<int:course_id>/lessons/<int:lesson_id>/progress', RegisterProgressView.as_view(), name='register-progress'),
    path('students/<int:student_id>/progress', ProgressListView.as_view(), name='student-progress'),
    path('students/<int:student_id>/courses/<int:course_id>/progress', CourseProgressView.as_view(), name='student-course-progress'),
]
