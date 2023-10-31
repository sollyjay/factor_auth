from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from FactorApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('posts', views.MainView.as_view(), name='posts'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('profile/<str:email>', views.OtherProfileView.as_view(), name='otherprofile'),
    path('api/', include('FactorApp.api.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
