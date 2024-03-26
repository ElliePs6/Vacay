from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Companies, CustomUser,Admins,Employees

@receiver(post_save, sender=CustomUser)
def create_employee(sender, instance, created, **kwargs):
    if created and instance.user_type == 'employee':
        # Retrieve the join date and username from the instance
        join_date = instance.date_joined
        username = instance.username

        # Retrieve the company associated with the user
        company = instance.company

        # Check if the company exists and create the Employees instance
        if company:
            Employees.objects.create(
                user=instance,
                company=company,
                join_date=join_date,
                username=username
            )

@receiver(post_save, sender=CustomUser)
def create_company(sender, instance, created, **kwargs):
    if created and instance.user_type == 'company':        
        # Create associated Companies instance with provided companyname and hrname
        Companies.objects.create(
            user=instance,
            companyname=instance.companyname,
            hrname=instance.hrname
        )

        

@receiver(post_save, sender=CustomUser)
def create_admin(sender, instance, created, **kwargs):
    if created and instance.user_type == 'admin':
        Admins.objects.create(user=instance)