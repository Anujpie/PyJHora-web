from django import forms

class HoroscopeForm(forms.Form):
    name = forms.CharField(max_length=255)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time_of_birth = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label