from django import forms


class RegisterFrom(forms.Form):
    f_name = forms.CharField(
        label='First name', max_length=100, required=False)
    l_name = forms.CharField(label='Last name', max_length=100, required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(label="Phone number",
                            max_length=20, required=False)
    username = forms.CharField(label="Username", max_length=50, required=False)
    passw = forms.CharField(label="password", min_length=7, required=False)
    note = forms.CharField(label="note", max_length=200, required=False)
