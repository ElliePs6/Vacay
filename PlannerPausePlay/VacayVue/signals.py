from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Employee, Company, Admins

@receiver(post_save, sender=CustomUser)
def create_employee(sender, instance, created, **kwargs):
    if created and instance.user_type == 'employee':
        Employee.objects.create(
            user=instance,
            join_date=instance.join_date,
            company=instance.company,
            first_name=instance.first_name,
            last_name=instance.last_name
        )

@receiver(post_save, sender=CustomUser)
def create_company(sender, instance, created, **kwargs):
    if created and instance.user_type == 'company':
        # Assuming Companies model has a field named 'admin' to link to the admin user
        Company.objects.create(
            user=instance,
            name=instance.name,
            hr_name=instance.hr_name
        )

@receiver(post_save, sender=CustomUser)
def create_admin(sender, instance, created, **kwargs):
    if created and instance.user_type == 'admin':
        # Assuming Admins model is linked to CustomUser similar to Companies and Employees
        Admins.objects.create(user=instance)

# Update create_company signal to create employee during company creation
@receiver(post_save, sender=CustomUser)
def create_company_and_employee(sender, instance, created, **kwargs):
    if created and instance.user_type == 'company':
        if not hasattr(instance, 'company_profile'):
            # If the user doesn't have a related company instance, create one
            company = Company.objects.create(
                user=instance,
                name=instance.name,
                hr_name=instance.hr_name
            )
            Employee.objects.create(
                user=instance,
                company=company,
                first_name=instance.first_name,
                last_name=instance.last_name
            )
