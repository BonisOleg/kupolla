from django.urls import path
from .views import FaqView

app_name = 'faq'

urlpatterns = [
    path('', FaqView.as_view(), name='index'),
]
