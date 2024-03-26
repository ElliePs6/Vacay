from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employee', 'Employee'),
        ('company', 'Company'),
        ('admin', 'Admin'),
    )
    permissions = models.CharField(max_length=255, null=True, blank=True)  
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    role = models.CharField(max_length=100, null=True)  
    is_staff = models.BooleanField(default=False)  
    is_admin = models.BooleanField(default=False)
    company = models.ForeignKey('Companies', on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)

class Admins(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Companies(models.Model):
    companyID = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile', default=None)
    companyname = models.CharField(max_length=255, null=True)
    hrname = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.companyname


class Employees(models.Model):
    employeeID = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile', default=None, unique=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, related_name='employee_profiles', null=True)
    join_date = models.DateTimeField(null=True, blank=True)
    username = models.CharField(max_length=225, null=True)
    
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

    request_id = models.AutoField(primary_key=True)
    EmployID = models.ForeignKey(Employees,related_name='requests', blank=True, null=True, on_delete=models.CASCADE)
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