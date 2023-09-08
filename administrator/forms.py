from django import forms
from courses.models import Course, Notification
from users.models import User, Stream


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all())
    stream = forms.ModelChoiceField(queryset=Stream.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'courses', 'stream']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['courses'].widget.attrs['class'] = 'form-control'
        self.fields['stream'].widget.attrs['class'] = 'form-select'  # Стилизуйте виджет выбора потока



class CuratorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'courses']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['courses'].widget.attrs['class'] = 'form-control'



class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['course', 'message', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control-file'})


