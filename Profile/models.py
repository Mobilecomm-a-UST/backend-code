import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Image = models.ImageField(upload_to="media/")
    Employee_Name = models.CharField(max_length=100, null=False, blank=False)
    Employee_Code = models.CharField(max_length=100)
    Email = models.EmailField()
    Designation = models.CharField(max_length=500)
    Contact = models.BigIntegerField()
    Office_Address = models.TextField()
    Home_Address = models.TextField()
    COUNTRY = models.CharField(max_length=100, default="India")
    STATE = models.CharField(max_length=100, default="Delhi")
    Gender = models.CharField(max_length=100, null=False, blank=False)


    def save(self, *args, **kwargs):
        if self.pk is not None:
            original_profile = ProfileModel.objects.get(pk=self.pk)
            if original_profile.Employee_Name != self.Employee_Name:
                # Update the associated User model's username
                self.user.username = self.Employee_Name
                self.user.save()

        super(ProfileModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.Employee_Name

class userCircle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Circle=models.CharField(max_length=100)
    user_catagory=models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return f'User:{str( self.user)} | Circle:{str(self.Circle)} | Catagory:{str(self.user_catagory)}'