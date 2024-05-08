from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('employee', 'Employee'),
        ('company', 'Company'),
        ('admin', 'Admin'),
    ]
    email=models.EmailField(max_length=100,unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS =['user_type',]


    def __str__(self):
        return self.email


class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='company_profile')
    name = models.CharField(max_length=255)
    hr_name = models.CharField(max_length=255)
    afm = models.PositiveIntegerField(unique=True)  
    dou = models.CharField(max_length=50,null=True, blank=True)
    

    def __str__(self):
        return self.user.username
    

class LeaveType(models.Model):
    CHOICES = (
        ('Κανονική Άδεια', 'Κανονική Άδεια'),
        ('Αδεια Εξετάσεων Εργαζόμενων Σπουδαστών', 'Αδεια Εξετάσεων Εργαζόμενων Σπουδαστών'),
        ('Αδεια Εξετάσεων Μεταπτυχιακών Φοιτητών', 'Αδεια Εξετάσεων Μεταπτυχιακών Φοιτητών'),
        ('Αιμοδοτική Άδεια', 'Αιμοδοτική Άδεια'),
        ('Άδεια Άνευ Αποδοχών', 'Άδεια Άνευ Αποδοχών'),
        ('Άδεια Μητρότητας', 'Άδεια Μητρότητας'),
        ('Άδεια Πατρότητας', 'Άδεια Πατρότητας'),
    )
    MONTH_CHOICES = (
        (1, 'Ιανουάριος'),(2, 'Φεβρουάριος'),(3, 'Μάρτιος'),(4, 'Απρίλιος'),
        (5, 'Μάιος'),(6, 'Ιούνιος'),(7, 'Ιούλιος'),(8, 'Αύγουστος'),
        (9, 'Σεπτέμβριος'),(10, 'Οκτώβριος'),(11, 'Νοέμβριος'),(12, 'Δεκέμβριος'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="leave_types")
    name = models.CharField(max_length=100, choices=CHOICES,default='Κανονική Άδεια')
    default_days = models.PositiveIntegerField(default=1)
    reset_month = models.IntegerField(choices=MONTH_CHOICES, default=1)

    class Meta:
        unique_together = ['user', 'name']
        

    def __str__(self):
        return self.name



class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    join_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=150, null=True)
    company = models.ForeignKey('Company', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Request(models.Model):    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="employee_requests")
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    is_pending = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"Leave request for {self.user.username}"
    
class Balance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    default_days = models.PositiveIntegerField(default=0)
    used_days = models.PositiveIntegerField(default=0)
    remaining_days = models.IntegerField(default=0)


'''






class Holidays(models.Model):
    HolidayID = models.AutoField(primary_key=True)
    HolidayName = models.CharField(max_length=255)
    Date = models.DateField()


class CustomHolidays(models.Model):
    CustomHolidayID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    HolidayName = models.CharField(max_length=255)
    Date = models.DateField()


class Permissions(models.Model):
    PermissionID = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=50)
    Feature = models.CharField(max_length=255)
    Allowed = models.BooleanField()

class ApprovalWorkflow(models.Model):
    WorkflowID = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=50)
    ApproverID = models.ForeignKey(Users, on_delete=models.CASCADE)
    MinimumApprovalLevel = models.IntegerField()
--------------------------------------------------------------
modela pou mallon den xreiazesai

class AuditTrail(models.Model):
    ACTION_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    AuditTrailID = models.AutoField(primary_key=True)
    RequestID = models.ForeignKey(Requests, on_delete=models.CASCADE)
    ActionTimestamp = models.DateTimeField(auto_now_add=True)
    ApproverID = models.ForeignKey(Users, on_delete=models.CASCADE)
    Action = models.CharField(max_length=50)
    Comments = models.TextField()


class Notification(models.Model):
   NotificationID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    Message = models.TextField()
    Timestamp = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=50)


'''