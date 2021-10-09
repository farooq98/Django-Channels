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

    path('issue/', IssueView.as_view()),
    path('get/issue/', GetIssue.as_view()),
    path('view/issues/', AllIssues.as_view()),
    path('like/issue/', ApproveIssueView.as_view()),
]