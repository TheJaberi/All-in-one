from django import forms

from users.models import Company


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices='', ** kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # adding choices to fields
        if choices:
            if choices.lower() == 'all in one':
                choices2 = (('Air Conditioner', 'Air Conditioner'),
                                                        ('Carpentry', 'Carpentry'),
                                                        ('Electricity',
                                                        'Electricity'),
                                                        ('Gardening', 'Gardening'),
                                                        ('Home Machines',
                                                        'Home Machines'),
                                                        ('House Keeping',
                                                        'House Keeping'),
                                                        ('Interior Design',
                                                        'Interior Design'),
                                                        ('Locks', 'Locks'),
                                                        ('Painting', 'Painting'),
                                                        ('Plumbing', 'Plumbing'),
                                                        ('Water Heaters', 'Water Heaters'))
            else:
                choices2 = [(choices, choices)]
            self.fields['field'].choices = choices2
        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'

        self.fields['name'].widget.attrs['autocomplete'] = 'off'


class RequestServiceForm(forms.Form):
    address = forms.CharField(max_length=40)
    service_hours = forms.IntegerField(min_value=1, max_value=24)
    
    def __init__(self, *args, **kwargs):
        super(RequestServiceForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Address'
        self.fields['service_hours'].widget.attrs['placeholder'] = 'Enter Service Hours'
        self.fields['address'].widget.attrs['autocomplete'] = 'off'
        self.fields['service_hours'].widget.attrs['autocomplete'] = 'off'
        self.fields['address'].widget.attrs['style'] = 'width: 100%'
        self.fields['service_hours'].widget.attrs['style'] = 'width: 100%'



