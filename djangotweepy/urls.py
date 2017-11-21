"""djangotweepy URL Configuration
"""
from django.conf.urls.static import static
from django.conf.urls import *
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    # redirect all urls to the twitter_auth app
    url(r'^admin/', admin.site.urls),
    url(r'^', include('twitter_auth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
