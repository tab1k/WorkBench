from django import forms
from comments.models import Comment
from courses.models import Lesson, Module


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class LessonCreationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Название урока'}),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4}),
        required=False
    )
    zoom_link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ссылка на Zoom'}),
        required=False
    )
    start_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Дата и время начала'}),
        required=False
    )
    video = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Видео'}),
        required=False
    )
    learn_documentation = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}),
        required=False
    )

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'zoom_link', 'start_datetime', 'video', 'learn_documentation']
