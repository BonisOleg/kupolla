from django.urls import path

from .views import ModelDetailView, ModelListView

app_name = 'catalog'

urlpatterns = [
    path('', ModelListView.as_view(), name='list'),
    path('<slug:slug>/', ModelDetailView.as_view(), name='detail'),
]
