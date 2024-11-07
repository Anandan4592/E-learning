from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course
from .forms import UserRegisterForm, CourseForm
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages


class RegisterView(View):
    """View used for registration"""

    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():            
            form.save()
            return redirect('loginpage')
        return render(request, 'register.html', {'form': form})



class CustomLoginView(LoginView):
    """view used for login"""

    template_name = 'loginpage.html'

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return 'admin_dashboard' 

        try:
            user_profile = user.userprofile
            if user_profile.role == 'Student':
                return 'student'  
            elif user_profile.role == 'Instructor':
                return 'instructor'
            
        except :          
            return 'loginpage' 

        
 
@login_required
def dashboard(request):
    """view which redirects user to their particular dashboards"""

    last_accessed_course_id = request.session.get('last_accessed_course')
    if last_accessed_course_id:
        last_accessed_course = Course.objects.get(id=last_accessed_course_id)
    else:
        last_accessed_course = None  

    user_profile = request.user.userprofile


    if user_profile.role == 'Student':
        all_courses = Course.objects.all()
        enrolled_courses = Course.objects.filter(students=request.user)
        return render(request, 'studentpage.html', {'enrolled_courses': enrolled_courses,'all_courses' : all_courses,'last_accessed_course': last_accessed_course})
    
    elif user_profile.role == 'Instructor':
        courses = Course.objects.filter(instructor=request.user)
        return render(request, 'instructorpage.html', {'courses': courses})
    
    else:
        return redirect('admin_dashboard')



@login_required
def course_create(request):
    """view for instructors to create course """

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('instructorpage')
        
    else:
        form = CourseForm()

    return render(request, 'courseform.html', {'form': form})



@login_required
def course_edit(request, id):
    """view for instructors to edit the course"""

    course = Course.objects.get(id=id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('instructorpage')
        
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courseform.html', {'form': form})



@login_required
def course_delete(request, id):
    """view for instructors to delete their courses"""

    course = Course.objects.filter(id=id, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect('instructorpage')



@login_required
def course_detail(request, id):
    """view to see the course in detail"""

    course = Course.objects.get(id=id)
    request.session['last_accessed_course'] = course.id
    return render(request, 'coursedetail.html', {'course': course})



@login_required
def course_enroll(request, id):
    """view for students to enroll into a course"""

    course = Course.objects.get(id=id)
    course.students.add(request.user) 
    return redirect('studentpage')



@login_required
def admin_dashboard(request):
    """view for logging in to admin dashboard"""

    users = User.objects.exclude(is_superuser=True).prefetch_related('userprofile')
    courses = Course.objects.all()
    return render(request, 'adminpage.html', {'users': users, 'courses': courses})



@login_required
def admincourse_delete(request, id):
    """view for admin to delete a course"""

    course = Course.objects.get(id=id)

    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect('admin_dashboard')



@login_required 
def delete_user(request, id):
    """view for admin to delete a user"""

    user = User.objects.get(id=id)

    if request.method == 'POST':

        if user.userprofile.role == 'Student':
            courses = Course.objects.filter(students=user)
            for course in courses:
                course.students.remove(user)
        
        elif user.userprofile.role == 'Instructor':
            courses = Course.objects.filter(instructor=user)
            courses.delete() 
            
        user_profile = user.userprofile
        user_profile.delete()  # Delete the user's profile
        user.delete()  # Finally, delete the user
        messages.success(request, "User and associated data deleted successfully.")
        return redirect('admin_dashboard')

    messages.error(request, "Invalid request.")
    return redirect('admin_dashboard')



@login_required
def admincourse_create(request):
    """view for admin to create course """

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')
        instructor_id = request.POST.get('instructor')
        instructor = User.objects.get(id=instructor_id)
        Course.objects.create(title=title, description=description, content=content, instructor=instructor)
        messages.success(request, 'Course added successfully.')
        return redirect('admin_dashboard')