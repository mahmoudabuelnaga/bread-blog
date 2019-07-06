from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('title','slug','author','created','status')
    list_filter   = ('author', 'created','status')
    search_fields = ('title','body')

admin.site.register(models.Category)

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('name','email','post','created','active')
    list_filter   = ('active','created','updated')
    search_fields = ('name','email','body')

admin.site.register(models.InstgramFeeds)