from .models import User,Post,PostLike,FollowUser,CommentPost
from rest_framework import serializers 


class createUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields  ='__all__'
    
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    bio = serializers.CharField()
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password  =serializers.CharField()
    
#post serializer 
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    
    title = serializers.CharField()
    descriptions = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    def update(self,instance,validated_data):
        if instance.user.id == validated_data['user'].id:
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError("You are not allowed to update this post.")

#post comment 
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentPost
        fields = '__all__'
    comment_text = serializers.CharField(max_length=264)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    def save(self, **kwargs):
        self.post = kwargs['post']
        return super().save(**kwargs)
    
#post like 
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

#follow the user 
class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = '__all__'
    user = serializers.PrimaryKeyRelatedField(read_only= True)
    follows = serializers.PrimaryKeyRelatedField(read_only=True)
    



        
