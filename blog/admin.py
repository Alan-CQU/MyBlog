
# Register your models here.
from django.contrib import admin
from .models import BlogType,Blog


@admin.register(Blog)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id","title","author","get_read_num","blog_type","create_time","last_update_time")
    ordering = ("id",) # id positive order -id,negetive


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name")
    ordering = ("id",)  # id positive order -id,negetive

