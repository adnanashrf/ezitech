from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from datetime import date

class authPage(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL, null=True, blank= True)

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class LeaveRequest(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[("approved", "Approved"), ("rejected", "Rejected"), ("pending", "Pending")], default="pending")

    def __str__(self):
        return f"LeaveRequest by {self.user.username} from {self.start_date} to {self.end_date} - {self.status}"

class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pictures/')

    def __str__(self):
        return f"{self.user.username}'s Profile Picture"
