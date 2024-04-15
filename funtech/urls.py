from rest_framework import routers
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
# from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView)

from django.conf import settings
from django.conf.urls.static import static

from events.views_event import EventViewSet
from events.views_applications import ApplicationAPIview
from events.views_favorites import FavoritesAPIView
from events.views_auxiliary import (
    ListDirectionAPIView,
    RetrieveDirectionAPIView,
    ListFormatAPIView,
    RetrieveFormatAPIView,
    ListEventStatusAPIView,
    RetrieveEventStatusAPIView,
    ListApplicationStatusAPIView,
    RetrieveApplicationStatusAPIView
    )


router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename="event")


urlpatterns = [
    path('api-auth/', include("rest_framework.urls")),  

    path('api/', include(router.urls)),
    path('api/events/<int:pk>/favorite/', FavoritesAPIView.as_view()),
    path('api/events/<int:pk>/application/', ApplicationAPIview.as_view()),
    
    path('api/direction/<int:pk>/', RetrieveDirectionAPIView.as_view()),
    path('api/direction/', ListDirectionAPIView.as_view()),

    path('api/format/<int:pk>/', RetrieveFormatAPIView.as_view()),
    path('api/format/', ListFormatAPIView.as_view()),

    path('api/eventstatus/<int:pk>/', RetrieveEventStatusAPIView.as_view()),
    path('api/eventstatus/', ListEventStatusAPIView.as_view()),

    path('api/applicationstatus/<int:pk>/', RetrieveApplicationStatusAPIView.as_view()),
    path('api/applicationstatus/', ListApplicationStatusAPIView.as_view()),

    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(
        url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
