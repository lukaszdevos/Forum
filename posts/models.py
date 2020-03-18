from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class PostModel(models.Model):
    topic = models.CharField(max_length=50)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    text_area = models.TextField()

    
    def __str__(self):
        return self.topic   
    
    def get_absolute_url(self):
        return reverse('posts:post_detail',kwargs={'pk':self.pk})
    
    def save(self,*args,**kwargs):
        if PostModel.save:
            super().save(*args,**kwargs)

            PostModelHistory.objects.create(
                text_area_edited = self.text_area,
                post = PostModel.objects.get(pk=self.pk)
            )

class PostModelHistory(models.Model):
    text_area_edited = models.TextField()
    history_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='posthistory')
    
    
    
    
    
    
    
class CommentsModel(models.Model):
    comment_text = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE,related_name='comments')
    
    def get_absolute_url(self):
        return reverse('posts:post_detail',kwargs={'pk':self.pk})
    
    
        
#just for fun to singals test     
class ArchivalModel(models.Model):
    topic = models.CharField(max_length=50)   
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    text_area = models.TextField()
    
