from django.urls import path
from .views import TechnologiesView

app_name = 'technologies'

urlpatterns = [
    path('', TechnologiesView.as_view(), name='index'),
]
