from django.shortcuts import render,redirect
from blogapp.forms import UserRegistrationForm,UserLoginForm,UserProfileForm,PasswordResetForm,BlogForm,ProfilePicResetForm,CommentForm
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from blogapp.models import UserProfile,Blogs,Comments
from django.contrib import messages
from django.utils.decorators import method_decorator

# Create your views here.

def signin_required(fun):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fun(request,*args,**kwargs)
        else:
            messages.error(request,"Please login")
            return redirect("signin")
    return wrapper


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"
    model = User
    success_url = reverse_lazy("signin")

    # def get(self,request,*args,**kwargs):
    #     form = self.form_class()
    #     return render(request,self.template_name,{"form":form})
    #
    # def post(self,request,*args,**kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("")
    #     else:
    #         return render(request, self.template_name, {"form": form})


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "sign-in.html"
    model = User

    # def get(self,request,*args,**kwargs):
    #     form = self.form_class()
    #     return render(request,self.template_name,{"form":form})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                return render(request, self.template_name, {"form": form})

@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView):
    model = Blogs
    form_class = BlogForm
    template_name = "home.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request,"post hasbeen seved")
        self.object = form.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blogs.objects.all().order_by("-posted_date")
        context["blogs"] = blogs
        comment_form = CommentForm()
        context["comment_form"] = comment_form
        return context

@method_decorator(signin_required,name="dispatch")
class AllBlogsView(TemplateView):
    template_name = "all-blogs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blogs.objects.all().order_by("-posted_date")
        context["blogs"] = blogs
        return context

@signin_required
def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class UserProfileView(CreateView):
    model = UserProfile
    template_name = "addprofile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.user=self.request.user
        messages.success(self.request,"profile hasbeen created")
        self.object = form.save()
        return super().form_valid(form)

@method_decorator(signin_required,name="dispatch")
class ViewMyprofileView(TemplateView):
    template_name = "viewprofile.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        user_blogs = Blogs.objects.filter(author=self.request.user)
        context["blogs"]=user_blogs
        return context


@method_decorator(signin_required,name="dispatch")
class PasswordResteView(FormView):
    template_name = "change-password.html"
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get("old_password")
            password1 = form.cleaned_data.get("new_password")
            password2 = form.cleaned_data.get("confirm_password")
            user = authenticate(request,username=request.user.username,password=old_password)
            if user:
                user.set_password(password2)
                user.save()
                messages.success(request,"Password changed successfully")
                return redirect("signin")
            else:
                messages.error(request,"invalid credentials")
                return render(request,self.template_name,{"form":form})

@method_decorator(signin_required,name="dispatch")
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "profile-update.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"Profile updated")
        self.object = form.save()
        return super().form_valid(form)

@method_decorator(signin_required,name="dispatch")
class ProfilePicUpdateView(UpdateView):
    model = UserProfile
    template_name = "propic-update.html"
    form_class = ProfilePicResetForm
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"profile picture updated successfully")
        self.object = form.save()
        return super().form_valid(form)


@signin_required
def add_comment(request,*args,**kwargs):
    if request.method == 'POST':
        blog_id = kwargs.get('post_id')
        blog = Blogs.objects.get(id=blog_id)
        user = request.user
        comment = request.POST.get("comment")
        Comments.objects.create(blog=blog , user=user , comment=comment)
        messages.success(request,"Comment Added")
        return redirect('home')

@signin_required
def add_like(request,*args,**kwargs):
    blog_id = kwargs.get("post_id")
    blog = Blogs.objects.get(id=blog_id)
    blog.liked_by.add(request.user)
    blog.save()
    return redirect("home")

@signin_required
def do_follow(request,*args,**kwargs):
    friend_id = kwargs.get("user_id")
    friend = User.objects.get(id=friend_id)
    request.user.users.following.add(friend)
    friend.save()
    messages.success(request,"You are started following"+ friend.username)
    return redirect("home")



