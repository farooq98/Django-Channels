from django.urls import path
from .views import PostView, CommentView, AllPosts, AllComments, LinkeView, GetPost, \
    IssueView, AllIssues, GetIssue, ApproveIssueView

urlpatterns = [
    path('post/', PostView.as_view()),
    path('get/post/', GetPost.as_view()),
    path('comment/', CommentView.as_view()),
    path('view/posts/', AllPosts.as_view()),
    path('view/comments/', AllComments.as_view()),
    path('like/post/', LinkeView.as_view()),

    path('post/', IssueView.as_view()),
    path('get/post/', GetIssue.as_view()),
    path('view/posts/', AllIssues.as_view()),
    path('like/post/', ApproveIssueView.as_view()),
]