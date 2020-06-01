from django.db import models
from django.contrib.auth.models import User
# from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    profile_img = models.ImageField(upload_to='profile', default='default.jpg', blank=True)

    def __str__(self):
        return f'{self.user} Profile'
    


    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img_input = Image.open(self.profile_img.path)

    #     if img_input.height > 100 or img_input.width > 100:
    #         img_output = (100, 100)
    #         img_input.thumbnail(img_output)
    #         img_input.save(self.profile_img.path)

    


    