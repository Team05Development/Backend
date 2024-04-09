from rest_framework import routers
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.conf import settings
from django.conf.urls.static import static

from events.views_event import EventViewSet
from events.views_applications import ApplicationAPIview
from events.views_favorites import FavoritesAPIView


router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename="event")


urlpatterns = [
    # path('pages/', include('pages.urls', namespace='pages')),
    path('api/', include(router.urls)),
    # path('api/ingredients/', ListIngredientsAPIView.as_view()),
    # path('api/ingredients/<int:pk>/', RetrieveIngredientsAPIView.as_view()),
    path('api/events/<int:pk>/favorite/', FavoritesAPIView.as_view()),
    path('api/events/<int:pk>/application/', ApplicationAPIview.as_view()),
    # path('api/tags/<int:pk>/', RetrieveTagsAPIView.as_view()),

    # path('api/tags/', ListTagsAPIView.as_view()),
    # path('api/tags/<int:pk>/', RetrieveTagsAPIView.as_view()),
    # path('api/recipes/<int:pk>/shopping_cart/', ShoppingCartAPIview.as_view()),
    # path('api/users/subscriptions/', SubscriptionsAPIView.as_view()),
    path('admin/', admin.site.urls),
    # path('api/', include('djoser.urls')),
    # path('api/auth/', include('djoser.urls.authtoken')),
    # path('api/users/<int:pk>/subscribe/', SubscribeAPIView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Funtech API",
#         default_version='v1',
#         description="Документация проекта Funtech",
#         contact=openapi.Contact(email="admin@funtech.ru"),
#         license=openapi.License(name="BSD License"),),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

# urlpatterns += [
#     url(r'^swagger(?P<format>\.json|\.yaml)$',
#         schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
#         name='schema-swagger-ui'),
#     url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
#         name='schema-redoc'),
# ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)