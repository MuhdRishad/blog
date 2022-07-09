# from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from blogapp.models import UserProfile,Blogs,Comments
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
   class Meta:
       model = User
       fields = [
           "first_name",
           "last_name",
           "username",
           "email",
           "password1",
           "password2"
       ]

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)
        widgets = {
            "bio" : forms.TextInput(attrs={"class" : "form-control"}),
            "phone" : forms.TextInput(attrs={"class" : "form-control"}),
            "date_of_birth" : forms.DateInput(attrs={"type":"date", "class" : "form-control"}),
            "gender" : forms.Select(attrs={"class":"form-control"})
        }


class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField()


class ProfilePicResetForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_pic"]
        widgets = {
            "profile_pic" : forms.FileInput(attrs={"class":"form-control"})
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ["title",
                  "description",
                  "image"
                  ]
        widgets = {
            "title" : forms.TextInput(attrs={"class":"form-control"}),
            "description" : forms.Textarea(attrs={"class":"form-control","rows":"3"}),
            "image" : forms.FileInput(attrs={"class":"form-control"})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]