from rest_framework import generics 
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response 
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView 
from App.models import Post, PostLike, CommentPost ,FollowUser,User 
from App.serializers import PostSerializer,CommentSerializer,PostLikeSerializer,FollowUserSerializer


class PostApiView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    queryset = Post.objects.all()
    serializer_class = PostSerializer 
    
#get the post 
class RetrivePostView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


#update the post 
class UpdatePost(generics.UpdateAPIView):
    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    #update the post 
    def put(self,request,pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'success':True,'message':"Update Post Successfully!!"})
        else:
            print(serializer.errors)
            return Response({'success':False,'msessage':"Something is went worng sorry try again for update post"})
        
#delete the post 
class DeletePostView(generics.DestroyAPIView):
    #authentication part 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #get the delete 
    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs['pk']
            post = Post.objects.get(id=pk)
            if post.user.id == request.user.id:
                self.perform_destroy(post)
                return Response({'success':True,'message':"Post has been deleted Successfully!!"})
            else:
                return Response({"success":False, "message":"You Dont Have Permission To delete This Post"})
        except ObjectDoesNotExist:
            return Response({"success":False, 'message':"Post Does not Exist!!"})
        
# retrive all user post 
class RetriveAllUserPostView(generics.ListAPIView):
    #get the permission 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def list(self, request, *args, **kwargs):
        user_post = Post.objects.filter(user=request.user.id)
        serializer = self.serializer_class(user_post,many=True)
        return Response({"success":True, "message":serializer.data})
    

# Comment user 
class CommentUserView(generics.CreateAPIView):
    authentication_classes  = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CommentPost.objects.all()
    serializer_class = CommentSerializer
    
    def get(self,request,pk):
        try:
            context = {
                'request':request
            }
            post = Post.objects.get(id=pk)
            comment = CommentPost.objects.filter(post=post)
            serializer = self.serializer_class(comment,many=True)
            return Response({'success':True, 'comment':serializer.data})
        except ObjectDoesNotExist:
            return Response({"success":False,"message":"post does not Exists"})
    def post(self, request,pk):
        try:
            context = {
                'request':request
            }
            post = Post.objects.get(id=pk)
            serializer = self.serializer_class(context=context,data=request.data)
            if serializer.is_valid():
                serializer.save(post=post)
                return Response({"success":True,"message":'comment added successfully'})
            else:
                print(serializer.errors)
                return Response({ "success": False, "message": "error adding a comment" })
        except ObjectDoesNotExist:
            return Response({'success':False,'message':"post does not Exists"})
        
#follow User 
class FollowUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FollowUser.objects.all()
    serializer_class = FollowUserSerializer
    
    def get(self,request,pk):
        following = FollowUser.objects.filter(user=request.user)
        followers = FollowUser.objects.filter(follows=request.user)
        
        following_serializer = FollowUserSerializer(following,many=True)
        followers_serializer = FollowUserSerializer(followers,many=True)
        
        
        
        return Response({'success':True,'follwers':followers_serializer.data,'following':following_serializer.data})
    
    def post(self,request,pk):
        try:
            following_user = User.objects.get(id=pk)
            follow_user = FollowUser.objects.get_or_create(user=request.user,follows=following_user)
            
            if not follow_user[1]:
                follow_user[0].delete()
                return Response({'success':True,'message':'unfollowed user'})
            else:
                return Response({'success':True,'message':'followed User'})
        
        except ObjectDoesNotExist:
            return Response({'success':False,'message':'following does not exists'})
        

class LikeUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    
    def get(self,request,pk):
        try:
            post = Post.objects.get(id=pk)
            liked_post = PostLike.objects.filter(post=post)
            like_serializer =  PostLikeSerializer(liked_post,many=True)
            return Response({'success':True,'message':like_serializer.data})
        except ObjectDoesNotExist:
            return Response({'success':False,'message':'post does not Exists'})
        
    def post(self,request,pk):
        try:
            post = Post.objects.get(id=pk)
            new_post_liked = PostLike.objects.get_or_create(user=request.user,post=post)
            if not new_post_liked[1]:
                new_post_liked[0].delete()
                return Response({'success':True,'message':'Unliked The Post'})
            else:
                return Response({'success':True,'message':'liked The post'})
        except: 
            return Response({'success':False,'message':'post does not Exists'})
        
        
        
    
        
        
        
    




    
    
    
    