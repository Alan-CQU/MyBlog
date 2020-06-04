from django.db import models
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum, ReadNumExpandMethod, ReadDetail
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


# Create your models here.
class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=30)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    #content = models.TextField()
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    # TODO 搞清楚这里面的内容
    read_details = GenericRelation(ReadDetail)

    def __str__(self):
        return "<Blog: %s>" % self.title

    # 定义显示的顺序
    class Meta:
        ordering = ["-create_time"]

