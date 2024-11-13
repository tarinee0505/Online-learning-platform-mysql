from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CourseEnrollForm(forms.Form):
    """Empty form for course enrollment"""
    pass

class CourseCreateForm(forms.ModelForm):
    """Form for creating and editing courses"""
    class Meta:
        model = Course
        fields = ['title', 'description', 'thumbnail', 'duration', 'price', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ModuleForm(forms.ModelForm):
    """Form for creating and editing course modules"""
    class Meta:
        model = Module
        fields = ['title', 'content', 'order', 'file_attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

class ProgressUpdateForm(forms.ModelForm):
    """Form for updating student progress"""
    class Meta:
        model = Progress
        fields = ['completed']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),  # Rating from 1 to 5
        }

class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['answer_text']
        widgets = {
            'answer_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your answer here...'}),
        }