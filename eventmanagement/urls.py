from django.contrib import admin
from django.urls import path,include
from event import views
from django.contrib.auth.views import LoginView,LogoutView
from event.views import CustomLoginView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('',include('eventCalendar.urls')),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('staffclick', views.staffclick_view),
    path('studentclick', views.studentclick_view),

    


    path('adminsignup', views.admin_signup_view),
    path('staffsignup', views.staff_signup_view,name='staffsignup'),
    path('studentsignup', views.student_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='college/adminlogin.html')),
    path('stafflogin', LoginView.as_view(template_name='college/stafflogin.html')),
    path('studentlogin', LoginView.as_view(template_name='college/studentlogin.html')),
    
    path('adminlogin/', CustomLoginView.as_view(), name='admin-login'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='college/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-staff', views.admin_staff_view,name='admin-staff'),
    path('admin-view-staff', views.admin_view_staff_view,name='admin-view-staff'),
    path('delete-staff-from-event/<int:pk>', views.delete_staff_from_event_view,name='delete-staff-from-event'),
    path('update-staff/<int:pk>', views.update_staff_view,name='update-staff'),
    path('admin-add-staff', views.admin_add_staff_view,name='admin-add-staff'),
    path('admin-approve-staff', views.admin_approve_staff_view,name='admin-approve-staff'),
    path('approve-staff/<int:pk>', views.approve_staff_view,name='approve-staff'),
    path('reject-staff/<int:pk>', views.reject_staff_view,name='reject-staff'),
    path('admin-view-staff-specialisation',views.admin_view_staff_specialisation_view,name='admin-view-staff-specialisation'),
    path('admin-opencourse', views.admin_opencourse_view,name='admin-opencourse'),

    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('delete-student-from-event/<int:pk>', views.delete_student_from_event_view,name='delete-student-from-event'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('admin-add-student', views.admin_add_student_view,name='admin-add-student'),
    path('admin-approve-student', views.admin_approve_student_view,name='admin-approve-student'),
    path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
    path('reject-student/<int:pk>', views.reject_student_view,name='reject-student'),
   

    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR Prin RELATED URLS-------------------------------------

#---------FOR staff RELATED URLS-------------------------------------
urlpatterns +=[
    path('staff-dashboard', views.staff_dashboard_view,name='staff-dashboard'),
    path('search', views.search_view,name='search'),

    path('staff-student', views.staff_student_view,name='staff-student'),
    path('staff-view-student', views.staff_view_student_view,name='staff-view-student'),
    path('staff-hod', views.staff_hod_view,name='staff-hod'),
    path('staff-opencourse', views.staff_opencourse_view,name='staff-opencourse'),
    path('staff-appointment', views.staff_appointment_view,name='staff-appointment'),
    path('staff-view-appointment', views.staff_view_appointment_view,name='staff-view-appointment'),
    path('staff-delete-appointment',views.staff_delete_appointment_view,name='staff-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
    path('staff-view-req-appointment', views.staff_view_req_appointment_view,name='staff-view-req-appointment'),
]




#---------FOR student RELATED URLS-------------------------------------
urlpatterns +=[

    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
    path('student-view-hod', views.student_view_hod,name='student-view-hod'),
    path('student-appointment', views.student_appointment_view,name='student-appointment'),
    path('student-book-appointment', views.student_book_appointment_view,name='student-book-appointment'),
    path('student-view-appointment', views.student_view_appointment_view,name='student-view-appointment'),
    path('student-view-staff', views.student_view_staff_view,name='student-view-staff'),
    path('searchstaff', views.search_staff_view,name='searchstaff'),
   path('opencourse', views.opencourse_view,name='opencourse'),
]


urlpatterns +=[
    path('head_login',views.head_login,name='head_login'),
    path('principal_dashboard',views.principal_dashboard,name='principal_dashboard'),
    path('principalstaff',views.principalstaff,name='principalstaff'),
    path('prin-appointment', views.p_admin_appointment_view,name='prin-appointment'),
    path('prin-home', views.prin_home,name='prin-home'),
    path('prin-view-appointment', views.p_admin_view_appointment_view,name='prin-view-appointment'),
    path('prin-add-appointment', views.p_admin_add_appointment_view,name='prin-add-appointment'),
    path('prin-approve-appointment', views.p_admin_approve_appointment_view,name='prin-approve-appointments'),
    path('prin/approve-appointment/<int:pk>', views.p_approve_appointment_view,name='prin-approve-appointment'),
    path('prin/reject-appointment/<int:pk>', views.p_reject_appointment_view,name='prin-reject-appointment'),

    path('p-admin-staff', views.P_admin_staff_view,name='p-admin-staff'),

    path('p-view-staff', views.p_view_staff_view,name='p-view-staff'),

    path('p-view-student', views.p_view_student_view,name='p-view-student'),

    path('prin-opencourse', views.prin_opencourse,name='prin-opencourse'),

    path('p-view-hod', views.P_view_hod,name='p-view-hod'),



]

