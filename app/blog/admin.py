from django.contrib import admin
from . import models


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'release_date', 'title')
    list_display_links = ('id', 'author')


class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    list_display_links = ('id', 'name')


admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment)
admin.site.register(models.Email, EmailAdmin)
