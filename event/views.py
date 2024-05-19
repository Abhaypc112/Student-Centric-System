from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'college/adminlogin.html'
    success_url = reverse_lazy('admin-dashboard')
    extra_context = {'error_message': 'Invalid username or password.'}

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/index.html')


#for showing signup/login button for admin(by )
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/adminclick.html')





#for showing signup/login button for staff(by )
def staffclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/staffclick.html')


#for showing signup/login button for student(by )
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/studentclick.html')

def opencourse_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/opencourse_view.html')



def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            if user.last_name.lower() in ['a11', 'b11','c11']:

               my_admin_group = Group.objects.get_or_create(name='ADMIN')
               my_admin_group[0].user_set.add(user)
               return HttpResponseRedirect('adminlogin')
            else:

               return render(request,'college/adminsignup.html',{'form': form, 'error': 'Invalid last name'})
    return render(request, 'college/adminsignup.html', {'form': form})




def staff_signup_view(request):
    userForm=forms.staffUserForm()
    staffForm=forms.staffForm()
    mydict={'userForm':userForm,'staffForm':staffForm}
    if request.method=='POST':
        userForm=forms.staffUserForm(request.POST)
        staffForm=forms.staffForm(request.POST,request.FILES)
        if userForm.is_valid() and staffForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staff=staffForm.save(commit=False)
            staff.user=user
            staff=staff.save()
            my_staff_group = Group.objects.get_or_create(name='staff')
            my_staff_group[0].user_set.add(user)
        return HttpResponseRedirect('stafflogin')
    return render(request,'college/staffsignup.html',context=mydict)


def student_signup_view(request):
    userForm=forms.studentUserForm()
    studentForm=forms.studentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.studentUserForm(request.POST)
        studentForm=forms.studentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.assignedstaffId=request.POST.get('assignedstaffId')
            student=student.save()
            my_student_group = Group.objects.get_or_create(name='student')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'college/studentsignup.html',context=mydict)






#-----------for checking user is staff , student or admin(by )
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_staff(user):
    return user.groups.filter(name='staff').exists()
def is_student(user):
    return user.groups.filter(name='student').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,staff OR student
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_staff(request.user):
        accountapproval=models.staff.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('staff-dashboard')
        else:
            return render(request,'college/staff_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.student.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'college/student_wait_for_approval.html')
    
    else:
        
        return redirect('logout')









#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    staffs=models.staff.objects.all().order_by('-id')
    students=models.student.objects.all().order_by('-id')
    #for three cards
    staffcount=models.staff.objects.all().filter(status=True).count()
    pendingstaffcount=models.staff.objects.all().filter(status=False).count()

    studentcount=models.student.objects.all().filter(status=True).count()
    pendingstudentcount=models.student.objects.all().filter(status=False).count()

    appointmentcount=models.EventDetails.objects.all().filter(status=True).count()
    pendingappointmentcount=models.EventDetails.objects.all().filter(status=False).count()
    mydict={
    'staffs':staffs,
    'students':students,
    'staffcount':staffcount,
    'pendingstaffcount':pendingstaffcount,
    'studentcount':studentcount,
    'pendingstudentcount':pendingstudentcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'college/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_staff_view(request):
    return render(request,'college/admin_staff.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_staff_view(request):
    staffs=models.staff.objects.all().filter(status=True)
    return render(request,'college/admin_view_staff.html',{'staffs':staffs})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_staff_from_event_view(request,pk):
    staff=models.staff.objects.get(id=pk)
    user=models.User.objects.get(id=staff.user_id)
    user.delete()
    staff.delete()
    return redirect('admin-view-staff')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_staff_view(request,pk):
    staff=models.staff.objects.get(id=pk)
    user=models.User.objects.get(id=staff.user_id)

    userForm=forms.staffUserForm(instance=user)
    staffForm=forms.staffForm(request.FILES,instance=staff)
    mydict={'userForm':userForm,'staffForm':staffForm}
    if request.method=='POST':
        userForm=forms.staffUserForm(request.POST,instance=user)
        staffForm=forms.staffForm(request.POST,request.FILES,instance=staff)
        if userForm.is_valid() and staffForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staff=staffForm.save(commit=False)
            staff.status=True
            staff.save()
            return redirect('admin-view-staff')
    return render(request,'college/admin_update_staff.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_staff_view(request):
    userForm=forms.staffUserForm()
    staffForm=forms.staffForm()
    mydict={'userForm':userForm,'staffForm':staffForm}
    if request.method=='POST':
        userForm=forms.staffUserForm(request.POST)
        staffForm=forms.staffForm(request.POST, request.FILES)
        if userForm.is_valid() and staffForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            staff=staffForm.save(commit=False)
            staff.user=user
            staff.status=True
            staff.save()

            my_staff_group = Group.objects.get_or_create(name='staff')
            my_staff_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-staff')
    return render(request,'college/admin_add_staff.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_staff_view(request):
    #those whose approval are needed
    staffs=models.staff.objects.all().filter(status=False)
    return render(request,'college/admin_approve_staff.html',{'staffs':staffs})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_staff_view(request,pk):
    staff=models.staff.objects.get(id=pk)
    staff.status=True
    staff.save()
    return redirect(reverse('admin-approve-staff'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_staff_view(request,pk):
    staff=models.staff.objects.get(id=pk)
    user=models.User.objects.get(id=staff.user_id)
    user.delete()
    staff.delete()
    return redirect('admin-approve-staff')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_staff_specialisation_view(request):
    staffs=models.staff.objects.all().filter(status=True)
    return render(request,'college/admin_view_staff_specialisation.html',{'staffs':staffs})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_opencourse_view(request):
    return render(request,'college/admin_opencourse.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'college/admin_student.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.student.objects.all().filter(status=True)
    return render(request,'college/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_event_view(request,pk):
    student=models.student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)

    userForm=forms.studentUserForm(instance=user)
    studentForm=forms.studentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.studentUserForm(request.POST,instance=user)
        studentForm=forms.studentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.status=True
            student.assignedstaffId=request.POST.get('assignedstaffId')
            student.save()
            return redirect('admin-view-student')
    return render(request,'college/admin_update_student.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    userForm=forms.studentUserForm()
    studentForm=forms.studentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.studentUserForm(request.POST)
        studentForm=forms.studentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            student=studentForm.save(commit=False)
            student.user=user
            student.status=True
            student.assignedstaffId=request.POST.get('assignedstaffId')
            student.save()

            my_student_group = Group.objects.get_or_create(name='student')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-student')
    return render(request,'college/admin_add_student.html',context=mydict)



#------------------FOR APPROVING student BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    #those whose approval are needed
    students=models.student.objects.all().filter(status=False)
    return render(request,'college/admin_approve_student.html',{'students':students})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    student=models.student.objects.get(id=pk)
    student.status=True
    student.save()
    return redirect(reverse('admin-approve-student'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_student_view(request,pk):
    student=models.student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')



#--------------------- FOR DISCHARGING student BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_student_view(request):
    students=models.student.objects.all().filter(status=True)
    return render(request,'college/admin_discharge_student.html',{'students':students})



#--------------for discharge student bill (pdf) download and printing
import io
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse






#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'college/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.EventDetails.objects.all().filter(status=True)
    return render(request,'college/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.EventReqForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.EventReqForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.staffId=request.POST.get('staffId')
            appointment.studentId=request.POST.get('studentId')
            appointment.staffName=models.User.objects.get(id=request.POST.get('staffId')).first_name
            appointment.studentName=models.User.objects.get(id=request.POST.get('studentId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'college/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.EventDetails.objects.all().filter(status=False)
    return render(request,'college/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.EventDetails.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.EventDetails.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ staff RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_dashboard_view(request):
    #for three cards
    studentcount=models.student.objects.all().filter(status=True,assignedstaffId=request.user.id).count()
    appointmentcount=models.EventDetails.objects.all().filter(status=True,staffId=request.user.id).count()
    
    #for  table in staff dashboard
    appointments=models.EventDetails.objects.all().filter(status=True,staffId=request.user.id).order_by('-id')
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.student.objects.all().filter(status=True,user_id__in=studentid).order_by('-id')
    appointments=zip(appointments,students)
    mydict={
    'studentcount':studentcount,
    'appointmentcount':appointmentcount,
    'appointments':appointments,
    'staff':models.staff.objects.get(user_id=request.user.id), #for profile picture of staff in sidebar
    }
    return render(request,'college/staff_dashboard.html',context=mydict)





@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_student_view(request):
    mydict={
    'staff':models.staff.objects.get(user_id=request.user.id), #for profile picture of staff in sidebar
    }
    return render(request,'college/staff_student.html',context=mydict)





@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_view_student_view(request):
    students=models.student.objects.all().filter(status=True,assignedstaffId=request.user.id)
    staff=models.staff.objects.get(user_id=request.user.id) #for profile picture of staff in sidebar
    return render(request,'college/staff_view_student.html',{'students':students,'staff':staff})


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_view_req_appointment_view(request):
    staff=models.staff.objects.get(user_id=request.user.id) #for profile picture of student in sidebar
    appointments=models.EventDetails.objects.all().filter(staffId=request.user.id)
    return render(request,'college/staff_view_req_appointment.html',{'appointments':appointments,'staff':staff})


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_hod_view(request):
    staff=models.staff.objects.get(user_id=request.user.id)
    return render(request,'college/staff_view_hod.html',{'staff':staff})

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_opencourse_view(request):
    staff=models.staff.objects.get(user_id=request.user.id)
    return render(request,'college/staff_opencourse_view.html',{'staff':staff})

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def search_view(request):
    staff=models.staff.objects.get(user_id=request.user.id) #for profile picture of staff in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    students=models.student.objects.all().filter(status=True,assignedstaffId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'college/staff_view_student.html',{'students':students,'staff':staff})



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_view_discharge_student_view(request):
    dischargedstudents=models.studentDischargeDetails.objects.all().distinct().filter(assignedstaffName=request.user.first_name)
    staff=models.staff.objects.get(user_id=request.user.id) #for profile picture of staff in sidebar
    return render(request,'college/staff_view_discharge_student.html',{'dischargedstudents':dischargedstudents,'staff':staff})



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_appointment_view(request):
    staff=models.staff.objects.get(user_id=request.user.id) #for profile picture of staff in sidebar
    return render(request,'college/staff_appointment.html',{'staff':staff})



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_view_appointment_view(request):
    staff=models.staff.objects.get(user_id=request.user.id) #for profile picture of staff in sidebar
    appointments=models.EventDetails.objects.all().filter(status=True,staffId=request.user.id)
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.student.objects.all().filter(status=True,user_id__in=studentid)
    appointments=zip(appointments,students)
    return render(request,'college/staff_view_appointment.html',{'appointments':appointments,'staff':staff})



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staff_delete_appointment_view(request):
    staff=models.staff.objects.get(user_id=request.user.id) #for profile picture of staff in sidebar
    appointments=models.EventDetails.objects.all().filter(status=True,staffId=request.user.id)
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.student.objects.all().filter(status=True,user_id__in=studentid)
    appointments=zip(appointments,students)
    return render(request,'college/staff_delete_appointment.html',{'appointments':appointments,'staff':staff})



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def delete_appointment_view(request,pk):
    appointment=models.EventDetails.objects.get(id=pk)
    appointment.delete()
    staff=models.staff.objects.get(user_id=request.user.id) #for profile picture of staff in sidebar
    appointments=models.EventDetails.objects.all().filter(status=True,staffId=request.user.id)
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.student.objects.all().filter(status=True,user_id__in=studentid)
    appointments=zip(appointments,students)
    return render(request,'college/staff_delete_appointment.html',{'appointments':appointments,'staff':staff})



#---------------------------------------------------------------------------------
#------------------------ staff RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ student RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    student=models.student.objects.get(user_id=request.user.id)
    staff=models.staff.objects.get(user_id=student.assignedstaffId)
    mydict={
    'student':student,
    'staffName':staff.get_name,
    'staffMobile':staff.mobile,
    'staffAddress':staff.address,
    'staffDepartment':staff.department,
    'admitDate':student.admitDate,
    }
    return render(request,'college/student_dashboard.html',context=mydict)

# def student_event_view(request):
#     student=models.student.objects.get(user_id=request.user.id) 
#     return render(request,'college/student_event.html',{'student':student})

def student_view_hod(request):
    student=models.student.objects.get(user_id=request.user.id) 
    return render(request,'college/student_view_hod.html',{'student':student})

def opencourse_view(request):
    student=models.student.objects.get(user_id=request.user.id) 
    return render(request,'college/opencourse_view.html',{'student':student})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_appointment_view(request):
    student=models.student.objects.get(user_id=request.user.id) #for profile picture of student in sidebar
    return render(request,'college/student_appointment.html',{'student':student})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_book_appointment_view(request):
    appointmentForm=forms.studentEventReqForm()
    student=models.student.objects.get(user_id=request.user.id) #for profile picture of student in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'student':student,'message':message}
    if request.method=='POST':
        appointmentForm=forms.studentEventReqForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('staffId'))
            desc=request.POST.get('description')

            staff=models.staff.objects.get(user_id=request.POST.get('staffId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.staffId=request.POST.get('staffId')
            appointment.studentId=request.user.id #----user can choose any student but only their info will be stored
            appointment.staffName=models.User.objects.get(id=request.POST.get('staffId')).first_name
            appointment.studentName=request.user.first_name #----user can choose any student but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('student-view-appointment')
    return render(request,'college/student_book_appointment.html',context=mydict)



def student_view_staff_view(request):
    staffs=models.staff.objects.all().filter(status=True)
    student=models.student.objects.get(user_id=request.user.id) #for profile picture of student in sidebar
    return render(request,'college/student_view_staff.html',{'student':student,'staffs':staffs})


def search_staff_view(request):
    student=models.student.objects.get(user_id=request.user.id) #for profile picture of student in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    staffs=models.staff.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'college/student_view_staff.html',{'student':student,'staffs':staffs})




@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_view_appointment_view(request):
    student=models.student.objects.get(user_id=request.user.id) #for profile picture of student in sidebar
    appointments=models.EventDetails.objects.all().filter(studentId=request.user.id)
    return render(request,'college/student_view_appointment.html',{'appointments':appointments,'student':student})




#------------------------ student RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'college/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'college/contactussuccess.html')
    return render(request, 'college/contactus.html', {'form':sub})





def head_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the provided username and password match the principal's credentials
        if username == 'principal' and password == '12345':
            # Check if the user with the specified username exists
            user = User.objects.filter(username=username).first()

            if not user:
                # If the user doesn't exist, create one
                user = User.objects.create_user(username=username, password=password)

            # Log in the user
            login(request, user)
            return redirect('prin-home')
        else:
            # Invalid login credentials
            return render(request, "login.html")

    return render(request, "login.html")




def principal_dashboard(request):
    return render(request,"principal_dashboard.html")

def principalstaff(request):
    return render(request,"principalstaff.html")


#-----------------APPOINTMENT START--------------------------------------------------------------------
def p_admin_appointment_view(request):
    return render(request,'prin/appointment.html')

def prin_home(request):
    return render(request,'prin/principal_home.html')

def p_admin_view_appointment_view(request):
    appointments = models.EventDetails.objects.all().filter(status=True, status2=True)

    return render(request,'prin/admin_view_appointment.html',{'appointments':appointments})



def p_admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.staffId=request.POST.get('staffId')
            appointment.studentId=request.POST.get('studentId')
            appointment.staffName=models.User.objects.get(id=request.POST.get('staffId')).first_name
            appointment.studentName=models.User.objects.get(id=request.POST.get('studentId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'prin/admin_add_appointment.html',context=mydict)



def p_admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments = models.EventDetails.objects.all().filter(status=True, status2=False)

    return render(request,'prin/admin_approve_appointment.html',{'appointments':appointments})



def p_approve_appointment_view(request,pk):
    appointment=models.EventDetails.objects.get(id=pk)
    appointment.status2=True
    appointment.save()
    return redirect(reverse('prin-view-appointment'))



def p_reject_appointment_view(request,pk):
    appointment=models.EventDetails.objects.get(id=pk)
    appointment.delete()
    return redirect('prin-view-appointment')



def P_admin_staff_view(request):
    return render(request,'college/admin_staff.html')



def p_view_staff_view(request):
    staffs=models.staff.objects.all().filter(status=True)
    return render(request,'prin/prin_view_staff.html',{'staffs':staffs})


def p_view_student_view(request):
    students=models.student.objects.all().filter(status=True)
    return render(request,'prin/prin_view_student.html',{'students':students})

def prin_opencourse(request):
    
    return render(request,'prin/prin_opencourse.html')

def P_view_hod(request):
    return render(request,'prin/prin_view_hod.html')