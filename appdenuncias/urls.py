from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from appdenuncias.view import my_view, my_view_parametros


urlpatterns = [
    path('admin/', admin.site.urls),
    path('denuncia/', include('denuncia.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )