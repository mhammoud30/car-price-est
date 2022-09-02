from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, Car, Conversation


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'description', 'carId', 'avatar']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name' ,'username', 'email','buyer', 'seller', 'phoneNum','password1' , 'password2']


class CarForm(ModelForm):
    class Meta: 
        model = Car
        fields = ['year', 'odometer', 'condition', 'transmission', 'model', 'price']


        