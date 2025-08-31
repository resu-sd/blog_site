from django.contrib import admin
from .models import User,Post,Category,Comment,Feedback,Like
# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Feedback)
admin.site.register(Like)