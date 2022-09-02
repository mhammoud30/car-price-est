from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique= True, null=True)
    buyer = models.BooleanField(default=True)
    seller = models.BooleanField(default=False)
    phoneNum = models.IntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class Car(models.Model):
    year = models.IntegerField()
    odometer = models.FloatField(max_length=10)
    condition = models.FloatField(max_length=4)
    transmission = models.IntegerField()
    model = models.CharField(max_length=50)
    price = models.FloatField(max_length=15)
    sellerId = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.model

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    sent_datatime = models.DateTimeField(auto_now=True)
    conversationId = models.ForeignKey('Conversation', on_delete= models.CASCADE)

    class Meta:
        ordering = ['sent_datatime']
    def __str__(self):
        return self.text[0:50]
    
    

class Conversation(models.Model):
     name = models.CharField(max_length=200) 
     carId = models.ForeignKey(Car, on_delete= models.CASCADE) 
     buyerId = models.ForeignKey(User,related_name='sender', on_delete=models.CASCADE)
     sellerId= models.ForeignKey(User,related_name='receiver', on_delete=models.CASCADE)
     
 
class Post(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    sellerId = models.ForeignKey(User, on_delete=models.CASCADE)
    carId = models.ForeignKey(Car, on_delete= models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(null=True)

    class Meta:
        ordering = ['-created'] 











    