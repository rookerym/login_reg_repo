from django.db import models
import re


class userManager(models.Manager):
    def validate_user(self, postdata):
        email_check =re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['f_name'])<2:
            errors['f_name']= 'First name must be at least 2 characters'
        if len(postdata['l_name'])<2:
            errors['l_name']= 'First name must be at least 2 characters'
        if not email_check.match(postdata['email']):
            errors['email'] = "Email must be valid format: x@y.zzz"
        if len(postdata['password'])<8:
            errors['password']='Password must be at least 8 characters'
        if postdata['password'] != postdata['conf_password']:
            errors['conf_password']='Password and confirm password must match'
        return errors


class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=userManager()

class MessageManager(models.Manager):
    def empty_valadator(self, postdata):
        errors=''
        if len(postdata['message']) < 1:
            errors='Messages must have content to post.'
        return errors

class PostMessage(models.Model):
    content= models.TextField()
    poster = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=MessageManager()

class Comment(models.Model):
    content=models.TextField(max_length=200)
    poster = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    message = models.ForeignKey(PostMessage, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)