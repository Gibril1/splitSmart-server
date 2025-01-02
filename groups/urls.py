from django.urls import path

from .views import GroupView, GroupDetailView

urlpatterns = [
    path('', GroupView.as_view(), name='groups'),
    path('<int:pk>/', GroupDetailView.as_view(), name='groups_detail'),
]