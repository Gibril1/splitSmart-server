from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from splitwise.permissions import UserEditDeletePermission
from .serializers import GroupSerializer
from .models import Groups


class GroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            # Retrieve a specific group by ID
            group = get_object_or_404(Groups, id=id, user=request.user)
            serializer = GroupSerializer(group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Retrieve all groups for the authenticated user
            groups = Groups.objects.filter(user=request.user)
            serializer = GroupSerializer(groups, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GroupDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [UserEditDeletePermission]
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer
