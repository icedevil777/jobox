from django.urls import path
from payment import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'payment'

urlpatterns = [
    path('new_tinkoff_card_payment', csrf_exempt(views.NewTinkoffCardPayment.as_view()),
         name='new_tinkoff_card_payment'),
]
