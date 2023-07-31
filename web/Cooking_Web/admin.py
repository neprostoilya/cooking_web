from django.contrib import admin
from .models import Category, Post



class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'watched', 'published', 'category', 'created_post', 'updated_post')
    list_display_links = ('id', 'title')
    list_editable = ('published',)
    readonly_fields = ('watched',)
    list_filter = ('title', 'category', 'watched')

admin.site.register(Category)
admin.site.register(Post, PostAdmin)