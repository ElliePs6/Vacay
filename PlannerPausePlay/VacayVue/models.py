from django.db import models
from django.contrib.auth.models import User


class Companies(models.Model):
    CompanyID = models.AutoField(primary_key=True)
    manager=models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    Email = models.EmailField()
    Companyname = models.CharField(max_length=255)

    #Εμφανιζει το ονομα στον admin και μπορουμε να δουμε ολα τα σχετικα
    def __str__(self):
        return self.Companyname
    
    
#Καθε υποληλος θα ανηκει σε μια εταιρια
class Employees(models.Model):
    EmployID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=255, unique=True)
    Firstname = models.CharField(max_length=255)
    Lastname= models.CharField(max_length=25, blank=True)#Του λεμε οτι δεν ειναι αναγκαστικο να το συμπληρωσεις
    Password = models.CharField(max_length=255)
    Role = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
   # Department = models.CharField(max_length=255)
    CompanyID = models.ForeignKey(Companies,blank=True,null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Username

#request ειναι 1:1 σχεση .Μια ετηση για καθε υπαλλοιλο
class Requests(models.Model):
    RequestID = models.AutoField(primary_key=True)
    EmployID = models.ForeignKey(Employees,blank=True,null=True, on_delete=models.CASCADE)
    StartDate = models.DateField()
    EndDate = models.DateField()
    Type = models.CharField(max_length=50)
    Status = models.CharField(max_length=50)
    Comments = models.TextField(blank=True)

    def __str__(self):
        return self.Type

class Calendar(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.title

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

    