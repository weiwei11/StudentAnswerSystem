"""StudentAnswerSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import notifications.urls
import permission
from django.conf import settings
from django.conf.urls import url, include, static
from django.contrib import admin

admin.autodiscover()
permission.autodiscover()
urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^StudentAnswerApp/', include('StudentAnswerApp.urls')),
                  url(r'^captcha/', include('captcha.urls')),
                  url(r'^comments/', include('django_comments.urls')),
                  url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
                  url(r'^avatar/', include('avatar.urls')),
                  url(r'^accounts/', include('registration.backends.hmac.urls')),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  url(r'^i18n/', include('django.conf.urls.i18n')),
              ] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static.static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)
