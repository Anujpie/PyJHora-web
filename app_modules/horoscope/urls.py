from django.urls import path
from app_modules.horoscope.views import HoroscopeInputView, HoroscopeResultView

app_name = 'horoscope'

urlpatterns = [
    path('', HoroscopeInputView.as_view(), name='horoscope_input'),
    path('result/', HoroscopeResultView.as_view(), name='horoscope_result'),
]
