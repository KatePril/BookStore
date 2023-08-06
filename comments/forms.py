from django import forms
from .models import CommentBook

class CommentBookForm(forms.ModelForm):
    class Meta:
        model = CommentBook
        fields = ('text')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }