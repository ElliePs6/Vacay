from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Companies, CustomUser

@receiver(post_save, sender=CustomUser)
def create_company(sender, instance, created, **kwargs):
    if created and instance.user_type == 'company':
        Companies.objects.create(
            user=instance,
            companyname='Default Company Name',
            hrname='Default HR Name',
        )
