# Create your views here.
from django.shortcuts import render,redirect
from .models import Category,Comment,Post,Like
from .forms import PostForm,CommentForm,UserCreationForm,FeedbackForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Count



# Create your views here.
def home(request):
    posts=Post.objects.all()
    categories = Category.objects.annotate(post_count=Count('post')).filter(post_count__gt=0)
    return render(request,'base.html',{'posts':posts,'categories':categories})

@login_required
def create_post(request):
    if not request.user.is_author:
        return HttpResponse("You are not authorized to create a post")
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES)

        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('home')
    else:
            form=PostForm()
    return render(request,'create_post.html',{'form':form})



def post_detail(request,id,slug):
    post=get_object_or_404(Post,id=id,slug=slug)
    comment=post.comments.all()
    likes_count=post.likes.count()
    form=CommentForm()
    if request.method=="POST":
        if 'comment_submit' in request.POST:
            form=CommentForm(request.POST)

            if form.is_valid():
                new_comment=form.save(commit=False)
                new_comment.user=request.user
                new_comment.post=post
                new_comment.save()

                return redirect("post_detail",id=post.id,slug=post.slug)

        elif 'like' in request.POST:
            if Like.objects.filter(user=request.user, post=post).exists():
                Like.objects.filter(user=request.user, post=post).delete()
            else:
              Like.objects.create(user=request.user,post=post)
            return redirect('post_detail', id=post.id, slug=post.slug)
        
        else:
            form = CommentForm()

    return render(request, 'post_detail.html', {
    'post': post,
    'comments': comment,
    'form': form,
    'likes_count': likes_count
})


   
                  
@login_required                
def edit_post(request,id,slug):
    post=get_object_or_404(Post,id=id,slug=slug)
    if not request.user.is_author:
        return HttpResponse("You are not authorized to edit this post")
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('post_detail',post.id,post.slug)
    else:
        form=PostForm(instance=post)
    
    return render(request,'edit_post.html',{'form':form})



@login_required
def delete_post(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    if not request.user.is_author:
        return HttpResponse('You are not authorized')

    if request.method == 'POST':
        post.delete()
        return redirect('home')






@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    
   
    if comment.user == request.user:
        post_id = comment.post.id
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post_detail', id=post_id, slug=post_slug)
    
   
    return redirect('post_detail', id=comment.post.id, slug=comment.post.slug)
def category_list(request):
    category=Category.objects.all()
    return render(request,'category_list.html',{'category':category})

def blog(request):
    posts=Post.objects.all()
    categories = Category.objects.annotate(post_count=Count('post')).filter(post_count__gt=0)
    category=Category.objects.all()
    return render(request,'blog.html',{'posts':posts,'categories':categories,'category':category})



def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            
            login(request, user)

            subject = "Welcome to Blogger's Haven"
            message = "Thank you for registering! We are glad to have you."
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]

            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
            except Exception as e:
                print("Email error:", e)
                messages.warning(request, "🎉 Account created, but email could not be sent.")

            messages.success(request, "🎉 Welcome! Your account has been created.")
            return redirect('home')  

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
           return HttpResponse( "Invalid username or password")
    return render(request,'login.html')
        
def logout_view(request):
    logout(request)
    return redirect ('home')



@login_required
def create_feedback(request):
    

    if request.method=="POST":
        form=FeedbackForm(request.POST)
        if form.is_valid():
           feedback= form.save(commit=False)
           feedback.user=request.user
           feedback.save()
           return redirect('home')
    
    else:
        form=FeedbackForm()

    return render(request, 'contact.html', {'form': form})




def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def search(request):
    query = request.GET.get('q', '')  
    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query)
        )

    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'search.html', context)


def privacy(request):
    return render(request,'privacy.html')

def category_list(request):
    query = request.GET.get('q', '').strip()  
    category_id = request.GET.get('category', '')  

    posts= Post.objects.all()  

    if query:
        posts = posts.filter(title__icontains=query)
    if category_id:
        posts = posts.filter(category_id=category_id)

    categories = Category.objects.all()  

    return render(request, 'category.html', {'posts': posts, 'categories': categories})
