from django.contrib import admin
from App.models import * 

# Register your models here.
admin.site.register(Post)
admin.site.register(CommentPost)
admin.site.register(User)
admin.site.register(PostLike)
admin.site.register(FollowUser)
