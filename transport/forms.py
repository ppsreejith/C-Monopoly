from django import forms
from transport.models import Transport, check_stops, check_no_states, TransportCreated, check_player
from django.core.exceptions import ValidationError

class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
    
    def clean(self):
        states = self.cleaned_data.get('states')
        if states:
            check_no_states(states)
        else:
            raise ValidationError("Please Enter States")
        return self.cleaned_data

class TransportCreatedForm(forms.ModelForm):
    class Meta:
        model = TransportCreated
    
    def clean(self):
        states = self.cleaned_data.get('states')
        transport = self.cleaned_data.get('transport')
        player = self.cleaned_data.get('player')
        if states and transport and player:
            check_stops(states,transport)
            check_player(transport,player)
        else:
            raise ValidationError("Please Enter All Fields")
        return self.cleaned_data