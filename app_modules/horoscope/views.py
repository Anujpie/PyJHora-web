from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from PyQt6.QtWidgets import QApplication

from jhora.ui.horo_chart_tabs import ChartTabbed
from jhora import utils
from _datetime import datetime
import sys

from app_modules.horoscope.forms import HoroscopeForm   


def except_hook(cls, exception, traceback):
    print('exception called')
    sys.__excepthook__(cls, exception, traceback)
sys.excepthook = except_hook

class HoroscopeInputView(FormView):
    template_name = 'horoscope/home.html'
    form_class = HoroscopeForm

    def form_valid(self, form):
        name = form.cleaned_data['name']
        gender = form.cleaned_data['gender']
        date_of_birth = form.cleaned_data['date_of_birth']
        time_of_birth = form.cleaned_data['time_of_birth']

        App = QApplication(sys.argv)
        loc = utils.get_place_from_user_ip_address()
        chart_type = 'south_indian'
        chart = ChartTabbed(chart_type=chart_type,show_marriage_compatibility=True)
        print('chart: ', chart)
        chart.chart_type(chart_type)
        chart.language('English')
        chart.gender(1 if gender == 'Male' else 0)

        if len(loc) == 4:
            chart.place(loc[0], loc[1], loc[2], loc[3])
        
        chart.date_of_birth(date_of_birth.strftime('%Y,%m,%d'))
        chart.time_of_birth(time_of_birth.strftime('%H:%M:%S'))
        chart.compute_horoscope(calculation_type='drik')
        print('chart: ', chart)
        
        result = chart.get_chart()
        print('result: ', result)

        # Store result in session (or database)
        self.request.session['horoscope_result'] = result
        return HttpResponseRedirect(reverse("horoscope:horoscope_result"))


class HoroscopeResultView(TemplateView):
    template_name = 'horoscope/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.request.session.get('horoscope_result', 'No result available')
        return context

