from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
    path('contacts/', views.ContactListView.as_view(), name='contact_list'),
]
