from django.urls import path
from . import views

urlpatterns = [
    path('visited_links/', views.DomainAPIView.as_view(http_method_names=['post']), name='visited_links'),
    path('visited_domains/', views.DomainAPIView.as_view(http_method_names=['get']), name='visited_domains'),
]
