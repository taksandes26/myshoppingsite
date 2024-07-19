from django.urls import path
from . views import payment_process, payment_completed, payment_cancelled


app_name = 'payment'

urlpatterns = [
    path('process/', payment_process, name='process'),
    path('completed/',payment_completed, name='completed'),
    path('cancelled', payment_cancelled, name='cancelled'),
]