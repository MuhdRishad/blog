from django.db import models
from django.contrib.auth.models import User
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


#MODEL FOR BLOGS
class Blogs(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=230)
    image = models.ImageField(upload_to="blogimages",null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
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