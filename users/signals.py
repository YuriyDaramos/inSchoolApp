from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == "users":
        for group_name in ["Students", "Teachers", "Administrators"]:
            Group.objects.get_or_create(name=group_name)
