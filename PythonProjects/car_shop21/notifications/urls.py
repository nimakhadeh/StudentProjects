from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('api/device/register/', views.RegisterDeviceView.as_view(), name='register_device'),
    path('api/location/update/', views.UpdateLocationView.as_view(), name='update_location'),
]