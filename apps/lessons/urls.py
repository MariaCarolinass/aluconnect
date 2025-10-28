from django.urls import path
from apps.lessons.views import (
    LessonListView, LessonCreateView,
    LessonDetailView, LessonUpdateView,
    LessonDeleteView
)

urlpatterns = [
    path('courses/<int:course_id>/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('courses/<int:course_id>/lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/delete/', LessonDeleteView.as_view(), name='lesson-delete'),
]
