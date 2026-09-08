from django.urls import path
from .views import ConfiguratorView

app_name = 'configurator'

urlpatterns = [
    path('', ConfiguratorView.as_view(), name='index'),
]
