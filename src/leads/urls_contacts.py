from django.urls import path
from .views import ContactsView

app_name = 'contacts'

urlpatterns = [
    path('', ContactsView.as_view(), name='index'),
]
