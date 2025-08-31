from django import forms
from .models import Post, Comment, User, Category, Feedback
from django.utils.text import slugify
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

class PostForm(forms.ModelForm):
   slug = forms.SlugField(
        max_length=200,
        required=False,  
        help_text="Leave blank to auto-generate from title."
    )
   class Meta:
        model=Post
        fields=['title','slug','content','category','image']
    
   def save(self,commit=True):
       post=super().save(commit=False)

       if not post.slug:
           post.slug=slugify(post.title)

       if commit:
           post.save()

       return post


class CommentForm(forms.ModelForm):
   
    class Meta:
         model=Comment
         fields=['content']
         widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add your comment here...'}),        
        } 

class UserCreationForm(BaseUserCreationForm):
    is_author = forms.BooleanField(required=False, initial=False, label="Are you an author?")
    class Meta:
     model = User
     fields = ['username', 'email', 'is_author', "password1", "password2"]     
    
        

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'message']

