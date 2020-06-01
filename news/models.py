from django.db import models

# Create your models here.


class NewsModel(models.Model):
    topic = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    news_img = models.URLField(max_length=500)
    url = models.URLField(max_length=500)
    
    