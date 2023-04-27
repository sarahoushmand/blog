from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')
    age = models.PositiveIntegerField(null=True)
    about = models.CharField(max_length=300, null=True)
    image = models.ImageField(upload_to='media', null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_author_profile(sender, instance, created, **kwargs):
    if created:
        AuthorProfile.objects.create(user=instance)
