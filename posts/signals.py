from django.db.models.signals import post_delete
from django.dispatch import receiver
from posts.models import PostModel, ArchivalModel

@receiver(post_delete, sender=PostModel)
def archival(sender, instance, using=ArchivalModel, **kwargs):
    if PostModel.delete:
        ArchivalModel.objects.create(text_area=instance.text_area, topic=instance.topic,
                                     created_by=instance.created_by, pub_date=instance.pub_date)