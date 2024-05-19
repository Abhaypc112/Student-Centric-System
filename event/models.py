from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



departments=[('ComputerScience','ComputerScience'),
('Literature','Literature'),
('ComputerApplication','ComputerApplication'),
('Mathematics','Mathematics'),
('History','History'),
('Instrumentation','Instrumentation')
]
class staff(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/staffProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/studentProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedstaffId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class EventDetails(models.Model):
    studentId=models.PositiveIntegerField(null=True)
    staffId=models.PositiveIntegerField(null=True)
    studentName=models.CharField(max_length=40,null=True)
    staffName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    status2=models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    description=models.TextField(max_length=500)
    start_date = models.DateTimeField(default=datetime.now, null=False)
    end_date = models.DateTimeField(default=datetime.now, null=False)
    def __str__(self):
        return self.title






