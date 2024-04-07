from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView

from .models_application import Application
from .serializers_application import ApplicationSerializer


User = get_user_model()


class ApplicationFutureListView(ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.current_user
        queryset = Application.objects.filter(
            datetime.fromtimestamp(Application.created_at) >= datetime.now(),
            Application.user.id == user.id
        )
        return queryset.order_by('-created_at')


class ApplicationFinishedListView(ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.current_user
        queryset = Application.objects.filter(
            datetime.fromtimestamp(Application.created_at) < datetime.now(),
            Application.user.id == user.id
        )
        return queryset.order_by('-created_at')


class ApplicationCreateView(CreateAPIView):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.current_user.id
        return super().create(request, *args, **kwargs)
