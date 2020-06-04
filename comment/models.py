from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name='comment',on_delete=models.DO_NOTHING)

    # 回复也是一种评论，这里使用自关联来进行优化，本来是可以拆分成两个表
    # related_name 用于从User表中获取对应的评论或者回复

    # 回复可以描述成树结构，root表示树的跟，也就是第一条评论
    root = models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.DO_NOTHING,blank=True)
    # parent 表示当前回复B的是上一条回复A
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.DO_NOTHING,blank=True)
    # reply_to表示上一条回复的作者名
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.DO_NOTHING,blank=True)




    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
