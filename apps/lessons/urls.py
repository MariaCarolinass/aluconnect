from django.urls import path
from apps.lessons.views import (
    LessonCreateView, LessonListView, LessonDetailView,
    LessonUpdateView, LessonDeleteView
)

urlpatterns = [
    path('courses/<int:course_id>/lessons', LessonListView.as_view(), name='lesson-list'),
    path('courses/<int:course_id>/lessons', LessonCreateView.as_view(), name='lesson-create'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>', LessonDetailView.as_view(), name='lesson-detail'),
    path('courses/<int:course_id>/lessons/update/<int:lesson_id>', LessonUpdateView.as_view(), name='lesson-update'),
    path('courses/<int:course_id>/lessons/delete/<int:lesson_id>', LessonDeleteView.as_view(), name='lesson-delete'),
]
