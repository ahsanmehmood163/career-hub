from django.urls import path
from . import views
urlpatterns = [
    path('', views.IndexView.as_view(), name='index_page'),
    path('post_detail/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/read-later', views.ReadLaterView.as_view(), name='read_later'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('create_user', views.CreateUserView.as_view(), name='create_user'),
    path('login', views.LoginView.as_view(), name='login'),
    path('login_auth', views.LoginAuthView.as_view(), name='login_auth'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('all_courses', views.AllCoursesView.as_view(), name='all_courses'),
    path('course_detail/<int:id>', views.CourseDetailView.as_view(), name='course_detail'),
    path('album_detail/<int:id>', views.DetailAlbumView.as_view(), name='album_detail'),
    path('create_album', views.CreateAlbumView.as_view(), name='create_album'),
    path('student_dashboard', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('student_profile', views.DetailProfileView.as_view(), name='student_profile'),
    path('instructor_dashboard', views.InstructorDashboardView.as_view(), name='instructor_dashboard'),
    path('instructor_profile', views.InstructorProfileView.as_view(), name='instructor_profile'),
]
