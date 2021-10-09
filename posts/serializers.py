from rest_framework import serializers
from .models import Post, Comment, Like, Issue, IssueImages, IssueCounter



class CommentSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'created_at', 'email']
    
class LikeSerializer(serializers.ModelSerializer):
    
    email = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['email']
    
class PostSerializer(serializers.ModelSerializer):
    
    created_by = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.username')
    commented_by = CommentSerializer(source='comments', many=True, read_only=True)
    liked_by = LikeSerializer(source='likes', many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 
            'image_url', 
            'content',
            'created_at', 
            'edited_at',
            'created_by', 
            'email',
            'liked_by', 
            'commented_by', 
        ]

class IssueImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssueImages
        fields = ['id', 'image_url']
    
class IssueCounteerSerializer(serializers.ModelSerializer):
    
    email = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = IssueCounter
        fields = ['email']

class IssueSerializer(serializers.ModelSerializer):
    
    created_by = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.username')
    # assigned_to_name = serializers.ReadOnlyField(source='assign_to.name')
    # assigned_to_username = serializers.ReadOnlyField(source='assign_to.username')
    issue_images = IssueImageSerializer(source='images', many=True, read_only=True)
    liked_by = IssueCounteerSerializer(source='issue_counts', many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 
            'title',
            'content',
            'status',
            # 'assigned_to_name',
            # 'assigned_to_username',
            'landmark',
            'longitude',
            'latitude',
            'created_at', 
            'edited_at',
            'created_by', 
            'email',
            'issue_images', 
            'liked_by',
        ]

