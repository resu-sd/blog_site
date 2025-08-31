# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text  import slugify
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(unique=True)
    bio=models.TextField(max_length=500,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_author=models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name



class Post(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True,blank=True)
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='post')
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name='post')
    image=models.ImageField(upload_to='post_images/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  
       
    def __str__(self):
       return self.title
    
class Feedback(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="feedbacks")
   subject=models.CharField(max_length=200)
   message=models.TextField()
   created_at=models.DateTimeField(auto_now_add=True)


   def __str__(self):
      return f"Feedback from {self.user.username}"
   
   def save(self, *args, **kwargs):
    super().save(*args, **kwargs)  

    send_mail(
            subject=f"Feedback from {self.user.username}: {self.subject}",
            message=self.message,
            from_email=settings.EMAIL_HOST_USER,  
            recipient_list=[settings.EMAIL_HOST_USER], 
            fail_silently=False,
        )
 

    


class Comment(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
   content=models.TextField()
   post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
   created_at=models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"Comment by {self.user.username} on{self.post.title}"
   
class Like(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
   post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
   created_at=models.DateTimeField(auto_now_add=True)


   def __str__(self):
      return f'{self.user.username} like{self.post.title}'

   




 


