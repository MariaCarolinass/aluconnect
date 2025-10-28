from django.urls import path
from apps.instructors.views import (
    InstructorListView, InstructorDetailView, 
    InstructorCreateView, InstructorUpdateView
)

urlpatterns = [
    path('instructors', InstructorListView.as_view(), name='instructor-list'),
    path('instructors/<int:id>', InstructorDetailView.as_view(), name='instructor-detail'),
    path('instructors/update/<int:id>', InstructorUpdateView.as_view(), name='instructor-update'),
    path('instructors/create', InstructorCreateView.as_view(), name='instructor-create'),
]
