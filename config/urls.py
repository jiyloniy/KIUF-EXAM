from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path
from django.urls import include
# open api schema view
schema_view = get_schema_view(
    openapi.Info(
        title="UserType API",
        default_version='v1',
        description="UserType API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="qodirxonyusufjanov5@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)
from django.conf.urls.i18n import i18n_patterns
from config import view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.index, name='index'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/', include('UserType.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/v1/', include('education.urls')),
    path('api/v1/', include('Exam.urls')),
    
]

