from django import forms
from .models import Comment, StudentDetail, User, Course
from . import constants

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "text": "Your Comment"
        }
        error_messages = {
            'user_name': {
                        'required': 'Please input this mandatory field',
                        'max_length': 'Please enter the shorter input'},
            'text': {
                'required': 'Please input this mandatory field',
                'max_length': 'Please enter the shorter input'}
        }


class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = StudentDetail
        fields = '__all__'
        labels = {
            "transcript": 'Upload Your Transcript',
            "major": "Select Major",
            "interest": "Select Interest",
            "skills": "Select Skills"
        }
        error_messages = {
            'transcript': {
                'required': 'This field is mandatory'
            },
            'major': {
                'required': 'This field is mandatory'
            },
            'interest': {
                'required': 'This field is mandatory'
            },
            'skill': {
                'required': 'This field is mandatory'
            }
        }


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'signup_as', 'major', 'phone_no', 'mobile_no', 'github',
                  'twitter', 'address', 'image']
        label = {
            'signup_as': 'Signup_As',
            'major': 'Select Major',
            'phone_no': 'Phone_No',
            'mobile_no': 'Mobile_No',
            'github': 'Github Account',
            'twitter': 'Twitter Account',
            'address': 'Address',
            'image': 'Upload Transcript',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'signup_as']
        label = {
            'username': 'Enter Username',
            'password' : 'Enter Password',
            'signup_as' : 'Signup As'
        }

        widgets = {
            'password': forms.PasswordInput()
        }


class CreateAlbumForm(forms.Form):
    name = forms.CharField(max_length=30, label='Enter Album Name')


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
