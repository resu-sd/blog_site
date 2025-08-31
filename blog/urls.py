



from django.urls import path
from .views import *


urlpatterns = [
   
    path('',home,name='home'),
    path('post/create',create_post,name='create_post'),
    path('post_detail/<int:id>/<slug:slug>/', post_detail, name='post_detail'),
    path('edit_post/<int:id>/<slug:slug>/',edit_post ,name='edit_post'),
    path('delete_post/<int:id>/<slug:slug>/',delete_post,name='delete_post'),
    path('category_list/',category_list,name='category_list'),
    path('login_view/',login_view,name='login_view'),
    path('logout_view/',logout_view,name='logout_view'),
    path('register/',register,name='register'),
    path('create_feedback/',create_feedback,name='create_feedback'),
    path('delete_comment/<int:id>/',delete_comment,name='delete_comment'),
    path('blog/', blog, name='blog'),
    path('about/', about, name='about'),
    path('contact/',contact, name='contact'),
    path('search/',search,name='search'),
    path('privacy/',privacy,name='privacy'),
    
    ]

