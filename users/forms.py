from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from ckeditor.fields import RichTextFormField

from shop.models import Book

class SingupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email','password1','password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'address', 'image', 'github', 'twitter', 'instagram', 'facebook')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'github':forms.TextInput(attrs={'class':'form-control'}),
            'twitter':forms.TextInput(attrs={'class':'form-control'}),
            'instagram':forms.TextInput(attrs={'class':'form-control'}),
            'facebook':forms.TextInput(attrs={'class':'form-control'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control'})
        self.fields['password'].widget.attrs.update({'class':'form-control'})


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', 'description', 'quantity', 'price', 'is_best_saled', 'category')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        book = super().save(commit=False)
        if commit:
            book.save()  
        return book