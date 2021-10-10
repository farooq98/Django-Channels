from django.contrib import admin
from .models import Post, Comment, Like, Issue, IssueImages, IssueCounter

# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    inlines = (CommentInline, )

# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post, PostAdmin)
admin.site.register(Issue)
admin.site.register(IssueImages)
admin.site.register(IssueCounter)
