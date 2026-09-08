from django.urls import path
from .views import BlogListView, BlogPostView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('<slug:slug>/', BlogPostView.as_view(), name='post'),
]
