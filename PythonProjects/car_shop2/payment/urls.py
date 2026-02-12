from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/<int:order_id>/', views.payment_process, name='process'),
    path('success/<int:order_id>/<str:tracking_code>/', views.payment_success, name='success'),
    path('failed/<int:order_id>/', views.payment_failed, name='failed'),
]
