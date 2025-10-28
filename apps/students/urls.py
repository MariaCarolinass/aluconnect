from django.urls import path
from apps.students.views import StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView

urlpatterns = [
    path('students', StudentListView.as_view(), name='student-list'),
    path('students/<int:id>', StudentDetailView.as_view(), name='student-detail'),
    path('students/create', StudentCreateView.as_view(), name='student-create'),
    path('students/<int:id>/update', StudentUpdateView.as_view(), name='student-update'),
]
