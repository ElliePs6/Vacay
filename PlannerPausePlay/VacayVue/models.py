from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('employee', 'Employee'),
        ('company', 'Company'),
        ('admin', 'Admin'),
    ]
    email=models.EmailField(max_length=100,unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS =['username',]


    def __str__(self):
        return self.email


class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='company_profile')
    name = models.CharField(max_length=255)
    hr_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    join_date = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=150, null=True)


    def __str__(self):
        return self.user.email

    

#request ειναι 1:1 σχεση .Μια ετηση για καθε υπαλλοιλο
class Requests(models.Model):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PENDING = 'pending'  # Status when request is submitted

    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    ]

    employeeID = models.ForeignKey(Employee,blank=True,null=True, on_delete=models.CASCADE)
    StartDate = models.DateTimeField(null=True, blank=True)
    EndDate = models.DateTimeField(null=True, blank=True)
    Type = models.CharField(max_length=50)
    Status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    Comments = models.TextField(blank=True)

    def __str__(self):
        return self.Type


class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = "tblevents"



'''



class TeamMembers(models.Model):
    TeamMemberID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    TeamLeadID = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='team_lead')
    CalendarViewPermission = models.BooleanField()


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

class Calendar(models.Model):
    STATUS_CHOICES = [
        ('holiday', 'Holiday'),
        ('day_off', 'Day Off'),
    ]
    Date = models.DateField(primary_key=True)
    Status = models.CharField(max_length=50)

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

class Permissions(models.Model):
    PermissionID = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=50)
    Feature = models.CharField(max_length=255)
    Allowed = models.BooleanField()

class TimeOffBalances(models.Model):
    BalanceID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    VacationBalance = models.IntegerField()
    SickLeaveBalance = models.IntegerField()
    #OtherLeaveBalance = models.IntegerField()
    Year = models.IntegerField()

class ApprovalWorkflow(models.Model):
    WorkflowID = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=50)
    ApproverID = models.ForeignKey(Users, on_delete=models.CASCADE)
    MinimumApprovalLevel = models.IntegerField()







#class Notification(models.Model):
#   NotificationID = models.AutoField(primary_key=True)
#    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
#    Message = models.TextField()
#    Timestamp = models.DateTimeField(auto_now_add=True)
#    Status = models.CharField(max_length=50)


'''