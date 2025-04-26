from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector

from .models import Ad


@receiver(post_save, sender=Ad)
def update_search_vector(sender, instance, **kwargs):
    Ad.objects.filter(id=instance.id).update(
        search_vector=(
                SearchVector("title", weight='A') +
                SearchVector("description", weight='B')
        )
    )
