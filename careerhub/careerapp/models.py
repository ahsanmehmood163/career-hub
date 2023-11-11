from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from . import constants

class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.caption}"


class Author(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name()}"


class Post(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="careerapp")
    slug = models.SlugField(unique=True)
    date = models.DateField(auto_now=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return f"{self.title} by {self.author}"


class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    text = models.TextField(max_length=200)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")



class StudentDetail(models.Model):
    transcript = models.ImageField(upload_to="careerapp/transcripts")
    major = models.CharField(max_length=100, choices=constants.major_choices, default="Select Your Major Here")
    skill = models.CharField(max_length=75, choices=constants.skill_choices, default="Select Your Skill Here")
    interests = models.CharField(max_length=75, choices=constants.interest_choices, default="Select Your Interest Here")
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.major}"


signup_choices = (
    ('Instructor', 'Instructor'),
    ('Student', 'Student')
)


class User(AbstractUser):
    signup_as = models.CharField(max_length=50, choices=signup_choices)
    image = models.ImageField(upload_to="careerapp/profile")
    major = models.CharField(max_length=70, null=True, choices=constants.skill_choices)
    phone_no = models.PositiveIntegerField(null=True)
    mobile_no = models.PositiveIntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    github = models.CharField(max_length=30, null=True)
    twitter = models.CharField(max_length=30, null=True)


class Course(models.Model):
    name = models.CharField(max_length=100)
    field = models.CharField(max_length=50, choices=constants.skill_choices)
    image = models.ImageField(upload_to='careerapp/course')
    file = models.FileField(upload_to='careerapp/course')

    def __str__(self):
        return f"{self.name}"


class Instructor(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.name}"


class Album(models.Model):
    name = models.CharField(max_length=50)
    course = models.ManyToManyField('Course', related_name='albums')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='albums')

    def __str__(self):
        return f"{self.name}"
