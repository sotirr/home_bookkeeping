from django.contrib import admin
from django.urls import path, include

from accounts.views import CustomLoginView


urlpatterns = [
    path('', CustomLoginView.as_view(redirect_authenticated_user=True)),
    path('', include('social_django.urls', namespace='social')),
    path('expenses/', include('expenses.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
