from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
user_model=get_user_model()

class Entry(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey(user_model,on_delete=models.SET_NULL,null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        verbose_name_plural='entries'
    
    def get_absolute_url(self):
        return reverse('blog:entry_detial',kwargs={'pk':self.pk})
    def __str__(self):
         return self.title

class Comment(models.Model):
    entry = models.ForeignKey(Entry,null=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)


    def __str__(self) -> str:
        return self.body