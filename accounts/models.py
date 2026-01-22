from django.db import models

# # Create your models here.

# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     # Add custom fields here
#     age = models.IntegerField(null=True, blank=True)



from django.contrib.auth.models import User
# Create your models here.
class circle_model(models.Model):
    user=models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    circle=models.CharField(max_length=100)
   

    def __str__ ( self ):
        return str(self.user)