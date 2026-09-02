from django import forms
from .models import Post
from django import forms
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Post, Category, Tag
class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'title',
            'featured_image',
            'category',
            'tags',
            'content',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your article title...'
                }
            ),

            'featured_image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'tags': forms.SelectMultiple(
                attrs={
                    'class': 'form-select tags-select'
                }
            ),

            'content': forms.Textarea(
                attrs={
                    'class': 'form-control content-editor',
                    'placeholder': 'Start writing your article...'
                }
            ),
        }

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'profile-input'
                }
            ),

            'first_name': forms.TextInput(
                attrs={
                    'class': 'profile-input',
                    'placeholder': 'Enter your first name'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'profile-input',
                    'placeholder': 'Enter your last name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'profile-input',
                    'placeholder': 'Enter your email address'
                }
            ),
        }

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            'name',
            'description',
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'profile-input',
                    'placeholder': 'Enter category name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'profile-input',
                    'placeholder': 'Enter category description',
                    'rows': 5
                }
            ),
        }

class TagForm(forms.ModelForm):
    class Meta:
            model = Tag
            fields = ['name']
            widgets = {
                'name': forms.TextInput(
                    attrs={
                        'class': 'profile-input',
                        'placeholder': 'Enter tag name'
                    }
                ),
            }

    def save(self, commit=True):
        from django.utils.text import slugify

        tag = super().save(commit=False)

        if not tag.slug:
            tag.slug = slugify(tag.name)

        if commit:
            tag.save()

        return tag