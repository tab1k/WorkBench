from django import forms
from blog.models import Post


class PostCreationForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Название поста'}),
        required=True
    )

    author = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Автор'}),
        required=True
    )

    author_url = forms.URLField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ссылка на автора'}),
        required=False  # Это поле не обязательное
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}),
        required=True
    )

    video = forms.URLField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ссылка на видео'}),
        required=False  # Это поле не обязательное
    )

    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4, 'placeholder': 'Текст поста'}),
        required=True
    )

    hashtag = forms.ChoiceField(
        choices=Post.HASHTAG,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        required=True
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'author_url', 'image', 'video', 'body', 'hashtag']
