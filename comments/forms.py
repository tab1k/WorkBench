from django import forms
from comments.models import Comment


class CommentForm(forms.ModelForm):
    reply_text = forms.CharField(widget=forms.Textarea, label='Ваш ответ', required=False)

    class Meta:
        model = Comment
        fields = ['text']
