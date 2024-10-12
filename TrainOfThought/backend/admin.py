from django.contrib import admin
from .models import Creator, Bot, Post, Comment

class CreatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'default_reputation', 'default_hatred', 'default_popularity', 'networth')
    search_fields = ('first_name', 'last_name')
    ordering = ('-default_reputation',)

class BotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'reputation', 'hatred', 'likeness', 'popularity', 'networth')
    search_fields = ('name',)
    ordering = ('-reputation',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot', 'content', 'likes', 'reposts')
    search_fields = ('content',)
    list_filter = ('bot',)
    ordering = ('-id',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','post', 'content', 'likes', 'reposts')
    search_fields = ('content',)
    list_filter = ('post',)
    ordering = ('-post',)

admin.site.register(Creator, CreatorAdmin)
admin.site.register(Bot, BotAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
