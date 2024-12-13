from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('detail', views.media_kit_detail, name='media_kit_detail'),
    path('media-kit/edit/<int:media_kit_id>/', views.edit_media_kit, name='edit_media_kit'),
	path('media-kit/<int:media_kit_id>/', views.media_kit_detail, name='media_kit_detail'),
    path('create-tag/', views.create_tag, name='create_tag'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)