from django.urls import path
from . import views

urlpatterns = [
    path('visited_links/', views.DomainAPIView.as_view(), name='visited_links'),
]
