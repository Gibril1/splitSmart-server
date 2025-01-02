from django.db import models
from users.models import User

# Create your models here.
class Groups(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    budget = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_group')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.get_username()} - {self.group.name}"