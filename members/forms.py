from django import forms



class OTPForm(forms.Form):
    otp = forms.CharField(label='Enter OTP', max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
