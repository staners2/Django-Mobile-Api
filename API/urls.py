from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('api/auth/registration', views.registration, name='registration'),
    path('api/auth/login', views.login, name='login'),
    path('api/countries', views.get_all_countries, name="get_all_countries"),
    path('api/countries/<int:id>', views.get_country, name="get_country"),
    path('api/userprofile/<int:user_profile_id>/country', views.update_country, name="update_country"),
    path('api/userprofile/<int:user_profile_id>/histories', views.show_histories, name="show_histories"),
    path('api/userprofile/<int:user_profile_id>/histories/<int:history_id>', views.delete_histories, name="delete_histories"),
]

# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)