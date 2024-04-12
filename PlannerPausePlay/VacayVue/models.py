from django.contrib.auth.models import AbstractUser
from django.db import models

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
    


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    join_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=150, null=True)
    company= models.ForeignKey(Company,blank=True,null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.email

    

#request ειναι 1:1 σχεση .Μια ετηση για καθε υπαλλοιλο
class Request(models.Model):
    REQUEST_TYPES_CHOICES= [
        ('κανονική άδεια','Κανονική Άδεια'),
        ('άδεια εξετάσεων εργαζόμενων σπουδαστών','Αδεια Εξετάσεων Εργαζόμενων Σπουδαστών'),
        ('άδεια εξετάσεων μεταπτυχιακών φοιτητών','Αεια Εξετάσεων Μεταπτυχιακών Φοιτητών'),
        ('αιμοδοτική άδεια','Αιμοδοτική Άδεια'),
        ('άδεια άνευ αποδοχών','Άδεια Άνευ Αποδοχών'),
        ('άδεια μητρλοτητας','Άδεια Μητρότητας'),
        ('άδεια πατρότητας','Άδεια Πατρότητας')
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="employee_request")
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=REQUEST_TYPES_CHOICES)
    description = models.TextField(blank=True)
    is_pending = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

'''






class Holidays(models.Model):
    HolidayID = models.AutoField(primary_key=True)
    HolidayName = models.CharField(max_length=255)
    Date = models.DateField()

class PublicHolidays(models.Model):
    HolidayID = models.AutoField(primary_key=True)
    Country = models.CharField(max_length=255)
    HolidayName = models.CharField(max_length=255)
    Date = models.DateField()

class CustomHolidays(models.Model):
    CustomHolidayID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    HolidayName = models.CharField(max_length=255)
    Date = models.DateField()


class TimeOffBalances(models.Model):
    BalanceID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    VacationBalance = models.IntegerField()
    SickLeaveBalance = models.IntegerField()
    #OtherLeaveBalance = models.IntegerField()
    Year = models.IntegerField()

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