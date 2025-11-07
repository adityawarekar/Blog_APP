from django.contrib import admin
from .models import Posts, Comment, Profile, Notification

admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Notification)
