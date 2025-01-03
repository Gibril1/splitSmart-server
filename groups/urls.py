from django.urls import path

from .views import GroupView, GroupDetailView, InviteMemberView

urlpatterns = [
    path('', GroupView.as_view(), name='groups'),
    path('<int:pk>/', GroupDetailView.as_view(), name='groups_detail'),
    path('invite/<int:id>/', InviteMemberView.as_view(), name='invite_member')
]