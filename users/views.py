from .serializers import RegistrationSerializer
from rest_framework.generics import CreateAPIView
from .models import  User


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

