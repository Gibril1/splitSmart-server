import logging

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.mail import EmailMessage, get_connection

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from splitwise.permissions import UserEditDeletePermission
from users.models import User
from .serializers import GroupSerializer
from .models import Groups, GroupMembership
from utils.invite import generate_invitation_email

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger instance
logger = logging.getLogger(__name__)


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




def generate_invite_link(group_id, user_id):
    base_url = settings.BASE_URL  
    return f"{base_url}invite/{group_id}/{user_id}/"

class InviteMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def get_group(self, id):
        try:
            return Groups.objects.get(id=id)
        except Groups.DoesNotExist:
            raise Http404("Group not found.")
        
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404("User with the provided email does not exist.")

    def post(self, request, id):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Please provide the email of the user to invite."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.get_user(email)
        group = self.get_group(id)

        
        if group.user != request.user:
            return Response(
                {"error": "You are not authorized to add members to this group."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        if GroupMembership.objects.filter(group=group, user=user).exists():
            return Response(
                {"error": "This user is already a member of the group."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        GroupMembership.objects.create(group=group, user=user)

        invite_link = generate_invite_link(group.id, user.id)

        message = generate_invitation_email(
            friend_name=group.user.username,
            group_name=group.name,
            description=group.description,
            start_date=group.start_date,
            invite_link=invite_link
        )

        # try:
        #     subject = f"Invitation from {group.user.username.capitalize()} to join {group.name.capitalize()}"
        #     recipient_list = [email]
        #     from_email = "gibril@reallygreattech.com"

        #     from django.core.mail import send_mail
        #     send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        #     logger.info(f"Invitation email sent to {email} for group {group.id}.")
        # except Exception as e:
        #     logger.error(f"Failed to send email to {email}: {e}")
        #     return Response(
        #         {"error": "The invitation could not be sent due to an internal error."}, 
        #         status=status.HTTP_503_SERVICE_UNAVAILABLE
        #     )

        from django.core.mail import EmailMessage

        try:
            subject = f"Invitation from {group.user.username.capitalize()} to join {group.name.capitalize()}"
            from_email = "gibril@reallygreattech.com"
            recipient_list = [email]

            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list,
            )
            email_message.content_subtype = "html"  # Set the content type to HTML
            email_message.send(fail_silently=False)

            logger.info(f"Invitation email sent to {email} for group {group.id}.")
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
            return Response(
                {"error": "The invitation could not be sent due to an internal error."}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


        return Response(
            {"message": "An invite has been sent to your friend."}, 
            status=status.HTTP_200_OK
        )