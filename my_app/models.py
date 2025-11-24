from django.db import models
from django.contrib.auth.models import User
import uuid

Gender_choices=(('M','Male'),
                ('F','Female'),
                ('O','Other'))
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gender=models.CharField(max_length=1,choices=Gender_choices,blank=True,null=True)
    dob=models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    hobbies = models.TextField(blank=True)
    avatar=models.ImageField(upload_to='avatars/',blank=True,null=True)
    email_verified=models.BooleanField(default=False)
    email_token=models.UUIDField(default=uuid.uuid4,editable=False)
    temp_password = models.CharField(max_length=128, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
class Course(models.Model):
    name = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)  
    fee = models.IntegerField()

    def __str__(self):
        return self.name

class Student_courses(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    signed_up_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('student','course')

   

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
