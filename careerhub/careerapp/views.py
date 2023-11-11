from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.urls import reverse
from .forms import CommentForm, StudentDetailForm, SignupForm, LoginForm, CreateAlbumForm, AddCourseForm
from .models import Post, Author, Tag, Comment, StudentDetail, User, Course, Album, Instructor
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    ordering = ["-date"]
    context_object_name = 'latest_posts'

    def get_queryset(self):
        query_set = super().get_queryset()
        data = query_set[:3]
        return data


class PostDetailView(LoginRequiredMixin, View):
    template_name = 'post_detail.html'
    model = Post

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        stored_post = request.session.get("stored_post")

        context = {
            'post': post,
            'post_tage': post.tags.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by("-id"),
        }
        return render(request, 'post_detail.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))
        context = {
            'post': post,
            'comment_form': comment_form,
            'post_tags': post.tags.all(),
            'comments': post.comments.all().order_by("-id")
        }
        return render(request, 'post-detail.html', context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        print(stored_posts)
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_post"] = False

        else:
            post = Post.objects.filter(id__in=stored_posts)
            context["posts"] = post
            context["has_post"] = True

        return render(request, 'read-later.html', context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        print(stored_posts)
        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")


class StudentDashboardView(LoginRequiredMixin, CreateView):
    template_name = 'studentdashboard.html'
    model = StudentDetail
    form_class = StudentDetailForm
    success_url = 'all_courses'


class SignupView(CreateView):
    template_name = 'signup.html'
    model = User
    form_class = SignupForm
    success_url = '/'


class CreateUserView(View):
    template_name = 'signup.html'
    model = User
    form = SignupForm

    def post(self, request):
        form = SignupForm(request.POST, request.FILES)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        signup_as = request.POST['signup_as']
        major = request.POST['major']
        phone_no = request.POST['phone_no']
        mobile_no = request.POST['mobile_no']
        github = request.POST['github']
        twitter = request.POST['twitter']
        address = request.POST['address']
        image = request.FILES['image']

        if form.is_valid():
            if User.objects.filter(username=username).exists():
                messages.info(request, "Email already exists")
                return HttpResponseRedirect('signup')
            elif User.objects.filter(email=email).exists():
                return HttpResponseRedirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password, signup_as=signup_as, major=major,
                                                phone_no=phone_no, mobile_no=mobile_no, github=github, twitter=twitter,
                                                address=address, image=image
                                                )
                user.save()
                user.albums.create(name='my_album')
                return HttpResponseRedirect('login')
        return render(request, 'signup.html', {'form': form})

    def get(self, request):
        form = SignupForm()

        return render(request, 'signup.html', {'form': form})


class LoginView(CreateView):
    template_name = 'login.html'
    model = User
    form_class = LoginForm


class LoginAuthView(View):
    template_name = 'login.html'
    form = LoginForm

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        signup_as = request.POST['signup_as']
        form = LoginForm(request.POST)
        login_user = User.objects.get(username=username, password=password)
        # user = authenticate(username=username, password=password)
        if login_user is not None:
            if signup_as == login_user.signup_as:
                # login(request, user)
                if signup_as == 'Student':
                    return HttpResponseRedirect('student_dashboard')
                elif signup_as == 'Instructor':
                    return HttpResponseRedirect('instructor_dashboard')
        else:
            messages.info(request, "Invalid user credentials")

        return render(request, 'login.html', {'form': form})

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('login')


class AllCoursesView(LoginRequiredMixin, ListView):
    template_name = 'all_courses.html'
    model = Course
    context_object_name = 'all_courses'


class CourseDetailView(LoginRequiredMixin, View):

    def get(self, request, id):
        all_albums = request.user.albums.all()
        course = Course.objects.get(id=id)
        context = {'course': course, 'all_albums': all_albums}
        return render(request, 'course_detail.html', context)

    def post(self, request, id):
        album_id = request.POST['selected_album']
        album = Album.objects.get(id=album_id)
        add_course = Course.objects.get(id=id)
        album.course.add(add_course)
        path = reverse('album_detail', args=[album.id])
        return HttpResponseRedirect(path)


class DetailAlbumView(LoginRequiredMixin, View):
    def get(self, request, id):
        album = request.user.albums.get(id=id)
        all_courses = album.course.all()
        context = {'album': album, 'all_courses': all_courses}
        return render(request, 'album_detail.html', context)


class DetailProfileView(LoginRequiredMixin, View):

    def get(self, request):
        user = User.objects.get(username=request.user)
        all_albums = user.albums.all()
        context = {'user': user, 'all_albums': all_albums}
        return render(request, 'student-profile.html', context)


class CreateAlbumView(View):

    def post(self, request):
        form = CreateAlbumForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            album = request.user.albums.create(name=name)
            path = reverse('album_detail', args=[album.id])
            return HttpResponseRedirect(path)

        return render(request, 'createalbum.html', {'form': form})

    def get(self, request):
        form = CreateAlbumForm()
        return render(request, 'createalbum.html', {'form': form})


class InstructorDashboardView(LoginRequiredMixin, CreateView):
    form_class = AddCourseForm
    template_name = 'instructordashboard.html'
    success_url = 'all_courses'


class InstructorProfileView(LoginRequiredMixin, View):
    def get(self, request):

        user = User.objects.get(username=request.user)
        context = {'user': user}
        return render(request, 'instructor-profile.html', context)



