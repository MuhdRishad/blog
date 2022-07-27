from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.

#MODEL FOR USERPROFILE
class UserProfile(models.Model):
    profile_pic = models.ImageField(upload_to="profilepics",null=True)
    bio = models.CharField(max_length=120)
    phone = models.CharField(max_length=125)
    date_of_birth = models.DateField(null=True)
    options = (
        ("male","male"),
        ("female","female"),
        ("other","other")
    )
    gender = models.CharField(max_length=20,choices=options,default="male")
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")
    following = models.ManyToManyField(User,related_name="followings",blank=True)

    @property
    def fetch_followings(self):
        return self.following.all()

    @property
    def fetch_followings_count(self):
        return self.fetch_followings.count()

    @property
    def get_followers(self):
        all_user_profile = UserProfile.objects.all()
        my_follwers = []
        for profile in all_user_profile:
            if self.user in profile.fetch_followings:
                my_follwers.append(profile)
                return my_follwers

    @property
    def get_followers_count(self):
        return len(self.get_followers())


                    # FOLLOW SUGGETIONS
    @property
    def get_invitations(self):
        all_user_profile = UserProfile.objects.all().exclude(user=self.user)   # fetching all user profile object except current user
        user_list = [user_profile.user for user_profile in all_user_profile] # fetching all users
        my_following_list = [user for user in self.fetch_followings]        # fetching all my following list
        invitations = [user for user in user_list if user not in my_following_list]    # removing my following from my all users
        return invitations


#MODEL FOR BLOGS
class Blogs(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=230)
    image = models.ImageField(upload_to="blogimages",null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="authors")
    posted_date = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User)

    @property
    def get_like_count(self):
        like_count = self.liked_by.all().count()
        return like_count

    @property
    def get_liked_users(self):
        liked_users = self.liked_by.all()
        users = [user.username for user in liked_users]
        return users



    def __str__(self):
        return self.title



#MODEL FOR COMMENTS
class Comments(models.Model):
    blog = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment = models.CharField(max_length=170)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment