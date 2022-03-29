from django.contrib import admin
from . import models

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'realesed_date', 'title')
    list_display_links = ('id', 'author')

admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Post, PostAdmin)
