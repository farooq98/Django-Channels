from django.db import models
from user_registration.models import UserModel


class Post(models.Model):

    user = models.ForeignKey(UserModel, on_delete = models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="comments")
    user = models.ForeignKey(UserModel, on_delete = models.CASCADE)
    content = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Like(models.Model):
    class Meta:
        unique_together = (('post', 'user'),)
    
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="likes")
    user = models.ForeignKey(UserModel, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Issue(models.Model):
    
    CHOICES = [
        ('PENDING', 'PENDING'),
        ('ACCEPTED', 'ACCEPTED'),
        ('INVALID', 'INVALID'),
        ('RESOLVED', 'RESOLVED')
    ]

    user = models.ForeignKey(UserModel, on_delete = models.CASCADE, related_name='issues_created')
    assign_to = models.ForeignKey(UserModel, on_delete = models.CASCADE, related_name='issues_assigned', null=True, blank=True)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=CHOICES, default='PENDING')
    landmark = models.CharField(max_length=50)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    lattitude = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class IssueImages(models.Model):
    image_url = models.CharField(max_length=2000)
    issue = models.ForeignKey(Issue, on_delete = models.CASCADE, related_name='images')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class IssueCounter(models.Model):
    class Meta:
        unique_together = (('issue', 'user'),)
    
    issue = models.ForeignKey(Issue, on_delete = models.CASCADE, related_name="issue_counts")
    user = models.ForeignKey(UserModel, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username