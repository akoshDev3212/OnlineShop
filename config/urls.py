"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('store.urls', 'store'), namespace='store')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
]

# Static fayllarni whitenoise (STATICFILES_STORAGE/WhiteNoiseMiddleware)
# serve qiladi, shuning uchun staticfiles_urlpatterns() kerak emas.
# Media fayllar uchun Render'da alohida obyekt-storage (S3, Cloudinary va h.k.)
# ulanmagani sababli, hozircha DEBUG holatidan qat'i nazar Django orqali
# serve qilinadi — aks holda mavjud rasm/mahsulot suratlari production'da
# ko'rinmay qoladi. Trafik ortsa buni tashqi storage'ga ko'chirish tavsiya etiladi.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)