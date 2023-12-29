from django import forms
from users.models import User


class CuratorCustomProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'country', 'city', 'address', 'stream', 'image']

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя'}),
        required=True
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Фамилия'}),
        required=True
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Почта'}),
        required=True
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'data-inputmask': "'mask': '+7 999 999 99 99'", 'placeholder': '+7 ___ ___ __ __'}
        ),
        required=False
    )

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4}),
        required=False
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}),
        required=False
    )

    country = forms.ChoiceField(
        choices=User.COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'required': True}),
        error_messages={'required': 'Please choose your country!'}
    )

    city = forms.ChoiceField(
        choices=User.CITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'required': True}),
        error_messages={'required': 'Please choose your city!'}
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your address', 'required': True}),
        error_messages={'required': 'Please enter your address!'}
    )
