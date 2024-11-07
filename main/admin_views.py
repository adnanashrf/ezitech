from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Attendance, LeaveRequest
from datetime import datetime
from django.db.models import Count, Q
from django.contrib import messages

@staff_member_required
def admin_dashboard(request):
    # Fetching the counts
    user_count = User.objects.count()  # Count of total users
    leave_request_count = LeaveRequest.objects.filter(status='pending').count()  # Count of pending leave requests
    attendance_count = Attendance.objects.count()  # Count of total attendance records

    # Fetching all users to display
    users = User.objects.all()

    # Count present and absent records
    total_present = Attendance.objects.filter(present=True).count()
    total_absent = Attendance.objects.filter(present=False).count()

    # Passing the counts to the template
    return render(request, 'admin_dashboard.html', {
        'user_count': user_count,
        'leave_request_count': leave_request_count,
        'attendance_count': attendance_count,
        'total_present': total_present,
        'total_absent': total_absent,
        'users': users
    })

@staff_member_required
def view_user_attendance(request, user_id):
    user = User.objects.get(id=user_id)
    attendance_records = Attendance.objects.filter(user=user)
    return render(request, 'view_user_attendance.html', {'attendance_records': attendance_records, 'user': user})

@staff_member_required
def edit_attendance(request, attendance_id):
    attendance = Attendance.objects.get(id=attendance_id)
    if request.method == 'POST':
        attendance.present = request.POST.get('present') == 'on'
        attendance.save()
        return redirect('view_user_attendance', user_id=attendance.user.id)
    return render(request, 'edit_attendance.html', {'attendance': attendance})

@staff_member_required
def delete_attendance(request, attendance_id):
    attendance = Attendance.objects.get(id=attendance_id)
    user_id = attendance.user.id
    attendance.delete()
    return redirect('view_user_attendance', user_id=user_id)

@staff_member_required
def leave_approval(request):
    # Retrieve all leave requests
    leave_requests = LeaveRequest.objects.all()

    # Handle form submission for approving or rejecting leave requests
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')

        # Use get_object_or_404 to handle cases where the leave request doesn't exist
        leave_request = get_object_or_404(LeaveRequest, id=leave_id)

        if action == 'approve':
            leave_request.status = "approved"  # Set status to approved
            leave_request.save()  # Save the approved status
            messages.success(request, f"Leave request by {leave_request.user.username} has been approved.")
        elif action == 'reject':
            leave_request.status = "rejected"  # Set status to rejected
            leave_request.delete()  # Save the rejected status
            messages.error(request, f"Leave request by {leave_request.user.username} has been rejected.")

    # Render the leave approval template with the leave requests
    return render(request, 'leave_approval.html', {'leave_requests': leave_requests})

@staff_member_required
def system_report(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        messages.warning(request, "there is no record")
        attendances = Attendance.objects.filter(date__range=[from_date, to_date])
        user_attendance_count = attendances.values('user__username').annotate(
            
            presents=Count('id', filter=Q(present=True)),
            absents=Count('id', filter=Q(present=False))
            
        )
        grades = {
            'A': 26,
            'B': 20,
            'C': 15,
            'D': 10,
        }

        def get_grade(present_days):
            for grade, days in grades.items():
                if present_days >= days:
                    return grade
            return 'F'

        for user_attendance in user_attendance_count:
            user_attendance['grade'] = get_grade(user_attendance['presents'])

        context = {
            'attendances': attendances,
            'user_attendance_count': user_attendance_count,
            'from_date': from_date,
            'to_date': to_date,
        }

        return render(request, 'system_report.html', context, )

    return render(request, 'system_report.html')

def user_report(request):
    if request.method == 'POST':
        from_user = request.POST.get('from_user')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        # Check if user exists
        try:
            user = User.objects.get(username=from_user)
        except User.DoesNotExist:
            messages.warning(request, "User not found.")
            return render(request, 'user_report.html')

        # Filter attendance records for the specific user within date range
        attendances = Attendance.objects.filter(user=user, date__range=[from_date, to_date])

        if not attendances.exists():
            messages.warning(request, "There are no attendance records for this user within the specified date range.")
        
        # Calculate present and absent counts for the user
        user_attendance_count = attendances.aggregate(
            presents=Count('id', filter=Q(present=True)),
            absents=Count('id', filter=Q(present=False))
        )

        grades = {
            'A': 26,
            'B': 20,
            'C': 15,
            'D': 10,
        }

        def get_grade(present_days):
            for grade, days in grades.items():
                if present_days >= days:
                    return grade
            return 'F'

        # Add the grade to user attendance data
        user_attendance_count['grade'] = get_grade(user_attendance_count['presents'])

        context = {
            'attendances': attendances,
            'user_attendance_count': user_attendance_count,
            'from_date': from_date,
            'to_date': to_date,
            'user': user,  # Pass user to display in template
        }

        return render(request, 'user_report.html', context)

    return render(request, 'user_report.html')