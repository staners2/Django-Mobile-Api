from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('api/auth/registration', views.registration, name='registration'),
    path('api/auth/login', views.login, name='login'),
    path('api/countries', views.get_all_countries, name="get_all_countries"),
]

# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)