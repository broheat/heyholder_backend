from django.db import models
from config.settings import base
from django.utils.text import slugify


class Post(models.Model):

    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post")
    code = models.CharField(max_length=6)
    title = models.CharField(db_index = True, max_length=200, verbose_name="제목")
    contents = models.TextField(verbose_name="내용")
    created_at = models.DateField(auto_now_add=True, verbose_name="작성일")
    amount = models.IntegerField()

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    contents = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(base.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, verbose_name="작성일")
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
