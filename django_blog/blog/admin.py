from django.contrib import admin
from .models import Post

class Post_Cus_D(admin.ModelAdmin):
    list_display = ('title','content','published_date','author')    

admin.site.register(Post, Post_Cus_D)