from django.shortcuts import render ,redirect

from django.contrib import messages
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from .models import Attendance, ProfilePicture, LeaveRequest
from .forms import LeaveRequestForm, ProfilePictureForm
from datetime import date



@login_required
def mark_attendance(request):
    if not Attendance.objects.filter(user=request.user, date=date.today()).exists():
        Attendance.objects.create(user=request.user)
        messages.warning(request, "Attendance marked.")
        return redirect('/')
    else:
        messages.warning(request, "You have already marked today's attendance.")
        return redirect('/')
        
@login_required
def view_attendance(request):
    # Retrieve attendance records for the current user
    attendance_records = Attendance.objects.filter(user=request.user)
    
    # Retrieve leave requests for the current user
    leave_requests = LeaveRequest.objects.filter(user=request.user)
    
    return render(request, 'viewath.html', {
        'attendance_records': attendance_records,
        'leave_requests': leave_requests
    })

@login_required
def leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user
            leave_request.save()
            messages.warning(request, "Your leave request is sent. Wait for the approval!")
            return redirect('/')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave_request.html', {'form': form})

@login_required
def edit_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            profile_picture, created = ProfilePicture.objects.get_or_create(user=request.user)
            profile_picture.picture = form.cleaned_data['picture']
            profile_picture.save()
            return redirect('/')
    else:
        form = ProfilePictureForm()
    return render(request, "edit_profile_picture.html", {'form': form})

@login_required(login_url='/login/')
def main(request):
    try:
        profile_picture = ProfilePicture.objects.get(user=request.user)
    except ProfilePicture.DoesNotExist:
        profile_picture = None
        
    return render(request , 'student.html' , {'profile_picture': profile_picture})
    

def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username= username).exists():
            messages.warning(request, "Invalid usename.")
            return redirect('/login/')

        user= authenticate(username=username, password=password)
        if user is None:
            messages.warning(request, "Invalid password.")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')
            
    return render(request , 'login.html')


def register(request):
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.warning(request, "The username already taken.")
            return redirect('/register/')
        
        user=User.objects.create(
         first_name=first_name,
         last_name=last_name,
         username=username,
        )

        user.set_password(password)
        user.save()
        messages.warning(request, "The account is successfully created.")

    return render(request , 'register.html')


def logoutPage(request):
    logout(request)
    return redirect('/login/')