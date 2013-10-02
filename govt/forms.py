from django import forms
from django.core.exceptions import ValidationError
from govt.models import LoansCreated, check_factories

class LoansCreatedForm(forms.ModelForm):
    class Meta:
        model = LoansCreated
    
    def clean(self):
        pk = self.instance.pk or 0
        mortaged_industries = self.cleaned_data.get('mortaged_industries')
        amount = self.cleaned_data.get('amount')
        time_remaining = self.cleaned_data.get('time_remaining')
        player = self.cleaned_data.get('player')
        if mortaged_industries and amount and time_remaining:
            check_factories(mortaged_industries,pk,amount,time_remaining, player)
        else:
            raise ValidationError("Please Enter All Fields")
        return self.cleaned_data
