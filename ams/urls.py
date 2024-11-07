
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from main import views ,admin_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.register, name='register'),

    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
    path('leave_request/', views.leave_request, name='leave_request'),
    path('edit_profile_picture/', views.edit_profile_picture, name='edit_profile_picture'),

    path('admin_dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('view_user_attendance/<int:user_id>', admin_views.view_user_attendance, name='view_user_attendance'),
    path('edit_attendance/<int:attendance_id>/', admin_views.edit_attendance, name='edit_attendance'),
    path('delete_attendance/<int:attendance_id>/', admin_views.delete_attendance, name='delete_attendance'),
    path('leave_approval/', admin_views.leave_approval, name='leave_approval'),
    path('system_report/', admin_views.system_report, name='system_report'),
    path('user_report/', admin_views.user_report, name='user_report'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)