
from django import forms
from .models import Profile
 
 
# creating a form
class BasicinfoForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Profile
 
        # specify fields to be used
        fields = [
            "first_name",
            "last_name",
            "phone",
            "company",
            "account_type",
            "address1",
            "address2",
            "zip_code",
        ]


class ProfileInfoForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Profile
 
        # specify fields to be used
        fields = [
            "profile_pic",
            "banner_pic",
            "profile_privacy",
        ]


class PayoutForm(forms.ModelForm):
    paypal_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'azhar@example.com', 'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ['paypal_email',]