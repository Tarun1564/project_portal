from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Feedback, Project

@receiver(post_save, sender=Feedback)
@receiver(post_delete, sender=Feedback)
def update_project_rating(sender, instance, **kwargs):
    project = instance.project
    avg = project.feedbacks.aggregate(Avg("rating"))["rating__avg"]
    project.rating = round(avg or 0, 2)
    project.save(update_fields=["rating"])
