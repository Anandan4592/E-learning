from django.urls import path
from .views import RegisterView,CustomLoginView
from. import views
from django.contrib.auth import views as auth_views 
urlpatterns = [
    path('', RegisterView.as_view(), name='register'), 
    path('loginpage', CustomLoginView.as_view(), name='loginpage'),  
    # path('dashboard', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('student', views.dashboard, name='studentpage'),
    path('instructor', views.dashboard, name='instructorpage'),  # For instructors
    # path('admin', views.dashboard, name='adminpage'),
    # Course-related URLs (Instructor-only views)
    path('course_create', views.course_create, name='course_create'),
    path('course_edit<int:id>', views.course_edit, name='course_edit'),
    path('course_delete<int:id>', views.course_delete, name='course_delete'),
    path('course_detail<int:id>', views.course_detail, name='course_detail'),

    # Enroll in a course (Student view)
    path('course_enroll<int:id>', views.course_enroll, name='course_enroll'),

    # Admin dashboard URL
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admincourse_delete<int:id>',views.admincourse_delete,name='admincourse_delete'),
    path('delete_user<int:id>',views.delete_user,name='delete_user'),
    path('admincourse_create',views.admincourse_create,name='admincourse_create')
    # Rolsed pe-baages (Student, Instructor)
      # For students

]
