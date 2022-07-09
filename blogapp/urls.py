from django.urls import path
from blogapp import views

urlpatterns = [
    path("accounts/signup", views.UserRegistrationView.as_view(), name="signup"),
    path("accounts/signin", views.UserLoginView.as_view(), name="signin"),
    path("home", views.IndexView.as_view(), name="home"),
    path("users/profile/add", views.UserProfileView.as_view(), name="add-profile"),
    path("user/profiles", views.ViewMyprofileView.as_view(), name="view-my-profile"),
    path("user/password/change", views.PasswordResteView.as_view(), name="password-change"),
    path("user/profile/change/<int:user_id>", views.ProfileUpdateView.as_view(), name="profile-update"),
    path("user/profilepic/change/<int:user_id>",views.ProfilePicUpdateView.as_view(),name="propic-update"),
    path("post/comment/<int:post_id>", views.add_comment, name="add-comment"),
    path("post/like/add/<int:post_id>",views.add_like,name="add-like"),
    path("signout", views.sign_out, name="logout")
]
