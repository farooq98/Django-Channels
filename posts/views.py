from rest_framework.pagination import PageNumberPagination
from core_files.authentication import PrivateAPI, PrivateListAPI
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, IssueSerializer
from rest_framework import status

from .models import Post, Comment, Like, Issue, IssueImages, IssueCounter

class PostView(PrivateAPI):

    def put(self, request):

        post = {
            'user': request.user,
            'content': request.data.get('content'),
            'image_url': request.data.get('image_url'),
        }

        post_obj = Post.objects.create(**post)

        return Response({
            "status": True,
            "message": "post created",
            "post_id": post_obj.id
        }, status=status.HTTP_200_OK)

    def post(self, request):

        try:
            post_obj = Post.objects.get(pk=request.data.get('post_id'), user=request.user)

            if request.data.get('content'):
                post_obj.content = request.data.get('content')

            if request.data.get('image_url'):
                post_obj.content = request.data.get('content')
            
            post_obj.save()

            return Response({
                "status": True,
                "message": "post updated"
            }, status=status.HTTP_200_OK)

        except Exception as e:
                return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_200_OK)


    def delete(self, request):

        try:
            post_obj = Post.objects.get(pk=request.data.get('post_id'), user=request.user)
            post_obj.delete()

        except Post.DoesNotExist:
            return Response({
                "status": False,
                "message": "Invalid post"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "post deleted"
        }, status=status.HTTP_200_OK)

class CommentView(PrivateAPI):

    def put(self, request):

        try:
            post_obj = Post.objects.get(
                pk = request.data.get('post_id'),
                workspace__id = request.data.get('workspace_id')
            )
        except Post.DoesNotExist:
            return Response({
            "status": False,
            "message": "post not found"
        }, status=status.HTTP_400_BAD_REQUEST)


        comment = {
            'user': request.user,
            'post': post_obj,
            'content': request.data.get('content')
        }

        comment_obj = Comment.objects.create(**comment)

        return Response({
            "status": True,
            "message": "comment created",
            "post_id": comment_obj.id
        }, status=status.HTTP_200_OK)

    def post(self, request):

        try:
            commnet_obj = Comment.objects.get(
                pk = request.data.get('comment_id'),
                user = request.user
            )
            if request.data.get('content'):
                commnet_obj.content = request.data.get('content')
                commnet_obj.save()

        except Comment.DoesNotExist:
            return Response({
                "status": False,
                "message": "comment not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "comment updated"
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            commnet_obj = Comment.objects.get(
                pk = request.data.get('comment_id'),
                user = request.user
            )
            commnet_obj.delete()
        except Comment.DoesNotExist:
            return Response({
                "status": False,
                "message": "comment not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "comment updated"
        }, status=status.HTTP_200_OK)

class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 25
        
class AllPosts(PrivateListAPI):
    
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):

        workspace_id = request.GET.get('workspace_id')
        self.queryset = self.queryset.filter(workspace__id=workspace_id)

        return super().get(request, *args, **kwargs)

class AllComments(PrivateListAPI):
    
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    # pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):

        post_id = request.GET.get('post_id')
        self.queryset = self.queryset.filter(post__id=post_id)

        return super().get(request, *args, **kwargs)

class LinkeView(PrivateAPI):

    def post(self, request):

        try:
            post_obj = Post.objects.get(
                pk = request.data.get('post_id'),
                workspace__id = request.data.get('workspace_id')
            )
        except Post.DoesNotExist:
            return Response({
                "status": False,
                "message": "post not found"
            }, status=status.HTTP_400_BAD_REQUEST)


        try:
            like = Like.objects.create(user=request.user, post=post_obj)
        except Exception as e:
            return Response({
                "status": False,
                "message": "Already liked"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "post liked",
            "liked_by": like.user.username
        }, status=status.HTTP_200_OK)

    def delete(self, request):

        try:
            post_obj = Post.objects.get(
                pk = request.data.get('post_id')
            )
        except Post.DoesNotExist:
            return Response({
                "status": False,
                "message": "post not found"
            }, status=status.HTTP_400_BAD_REQUEST)


        try:
            like = Like.objects.get(user=request.user, post=post_obj)
            like.delete()
        except Like.DoesNotExist:
            return Response({
                "status": False,
                "message": "Not liked"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "Like Removed"
        }, status=status.HTTP_200_OK)

class GetPost(AllPosts):

    pagination_class = None

    def get(self, request, *args, **kwargs):

        workspace_id = request.GET.get('workspace_id')
        post_id = request.GET.get('post_id')
        self.queryset = self.queryset.filter(pk=post_id, workspace__id=workspace_id)

        return super().get(request, *args, **kwargs)

class IssueView(PrivateAPI):
    
    def put(self, request):

        try:
            issue = {
                'user': request.user,
                'content': request.data.get('content'),
                'title': request.data.get('title'),
                'status': request.data.get('status'),
                'landmark': request.data.get('landmark'),
                'longitude': request.data.get('longitude'),
                'lattitude': request.data.get('lattitude'),
            }

            issue_obj = Issue.objects.create(**issue)

            for image in request.data.get('image_url', []):
                IssueImages.objects.create(image_url = image, issue = issue_obj)

            return Response({
                "status": True,
                "message": "Issue created",
                "issue_id": issue_obj.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        try:
            issue_obj = Issue.objects.get(pk=request.data.get('issue_id'), user=request.user)

            if request.data.get('content'):
                issue_obj.content = request.data.get('content')

            if request.data.get('assigned_to'):
                issue_obj.assign_to = request.user

            if request.data.get('status'):
                issue_obj.status = request.data.get('status')

            if request.data.get('title'):
                issue_obj.title = request.data.get('title')

            if request.data.get('landmark'):
                issue_obj.landmark = request.data.get('landmark')

            if request.data.get('lattitude') and request.data.get('longitude'):
                issue_obj.lattitude = request.data.get('lattitude')
                issue_obj.longitude = request.data.get('longitude')

            if request.data.get('image_url', []):
                for image in request.data.get('image_url'):
                    IssueImages.objects.create(image_url = image, issue = issue_obj)
            
            issue_obj.save()

            return Response({
                "status": True,
                "message": "issue updated"
            }, status=status.HTTP_200_OK)

        except Exception as e:
                return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_200_OK)


    def delete(self, request):

        try:
            issue_obj = Issue.objects.get(pk=request.data.get('issue_id'), user=request.user)
            issue_obj.delete()

        except Post.DoesNotExist:
            return Response({
                "status": False,
                "message": "Invalid post"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "issue deleted"
        }, status=status.HTTP_200_OK)

class AllIssues(PrivateListAPI):
    
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    pagination_class = CustomPagination

class GetIssue(AllIssues):
    
    pagination_class = None

    def get(self, request, *args, **kwargs):

        issue_id = request.GET.get('issue_id')
        self.queryset = self.queryset.filter(pk=issue_id)

        return super().get(request, *args, **kwargs)

class ApproveIssueView(PrivateAPI):
    
    def post(self, request):

        try:
            issue_obj = Issue.objects.get(
                pk = request.data.get('issue_id')
            )
        except Issue.DoesNotExist:
            return Response({
                "status": False,
                "message": "issue not found"
            }, status=status.HTTP_400_BAD_REQUEST)


        try:
            approve = IssueCounter.objects.create(user=request.user, issue=issue_obj)
        except Exception as e:
            return Response({
                "status": False,
                "message": "Issue Already Liked"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "Issue Liked",
            "liked_by": approve.user.username
        }, status=status.HTTP_200_OK)

    def delete(self, request):

        try:
            issue_obj = Issue.objects.get(
                pk = request.data.get('issue_id')
            )
        except Issue.DoesNotExist:
            return Response({
                "status": False,
                "message": "Issue not found"
            }, status=status.HTTP_400_BAD_REQUEST)


        try:
            remove_approval = IssueCounter.objects.get(user=request.user, issue=issue_obj)
            remove_approval.delete()
        except IssueCounter.DoesNotExist:
            return Response({
                "status": False,
                "message": "Like of issue Does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "Like from issue removed"
        }, status=status.HTTP_200_OK)