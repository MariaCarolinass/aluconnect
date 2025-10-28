from django.urls import path
from apps.courses.views import (
    CourseCreateView, CourseListView, CourseDetailView, CourseUpdateView,
    EnrollStudentView, StudentCoursesView, InstructorCoursesView
)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:id>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:id>/enroll/', EnrollStudentView.as_view(), name='course-enroll'),
    path('students/<int:id>/courses/', StudentCoursesView.as_view(), name='student-courses'),
    path('instructors/<int:id>/courses/', InstructorCoursesView.as_view(), name='instructor-courses'),
]
