from django.urls import path 
from App.Views.user import CreateUserView,LoginUserView,RetriveUserView,UpdateUserView,DestroyUserView
from App.Views.post import PostApiView,RetrivePostView,UpdatePost,DeletePostView,RetriveAllUserPostView,FollowUserView,LikeUserView,CommentUserView

urlpatterns = [
    path('api/create',CreateUserView.as_view()),
    path('api/login',LoginUserView.as_view()),
    path('api/users/<int:pk>',RetriveUserView.as_view()),
    path('api/users/update',UpdateUserView.as_view()),
    path('api/users/delete/<int:pk>',DestroyUserView.as_view()), 
    path('api/post/create',PostApiView.as_view()),
    path('api/post/<int:pk>',RetrivePostView.as_view()),
    path('api/post/update/<int:pk>/',UpdatePost.as_view()),
    path('api/post/delete/<int:pk>/',DeletePostView.as_view()),
    path('api/post/',RetriveAllUserPostView.as_view()),
    path('api/post/like/<int:pk>',LikeUserView.as_view()),
    path('api/post/comment/<int:pk>',CommentUserView.as_view()),
    path('api/post/comment/<int:pk>',CommentUserView.as_view()),
    path('api/follow/<int:pk>',FollowUserView.as_view()),
]
