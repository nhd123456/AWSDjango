from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from allauth.account.forms import SignupForm

Pay_choice = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class checkoutForm(forms.Form):
    str_adr = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Address'
    }))
    apt_adr = forms.CharField(required = False, widget=forms.TextInput(attrs={
        'placeholder': 'apt'
    }))
    country = CountryField(blank_label = 'Select Country').formfield(widget= CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    zip = forms.CharField()
    set_bill_adr = forms.BooleanField(required=False)
    save = forms.BooleanField(required=False)
    pay = forms.ChoiceField(widget = forms.RadioSelect(), choices = Pay_choice)

class signUP(SignupForm):
    first_name = forms.CharField(max_length=128, label = 'First Name')
    last_name = forms.CharField(max_length=128, label = 'Last Name')
    def save(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class couponForm(forms.Form):
    code = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholdeer': 'promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2',
    }))