from rest_framework.serializers import ModelSerializer
from .models import Groups, GroupMembership

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'

class GroupMembershipSerializer(ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = '__all__'