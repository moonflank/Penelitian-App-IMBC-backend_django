from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ImageAnalysisView

urlpatterns = [
    path('analyze/', ImageAnalysisView.as_view(), name='analyze-image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
