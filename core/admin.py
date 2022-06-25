from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models
# Register your models here.


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = ( 
        (None, {'fields': ('email' ,'password', 'username')}),
        (_('Personal Info'), {'fields': ('name', 'bio', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2')
            }),
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'content',]

class ContentAdmin(admin.ModelAdmin):
    list_display = ['author', 'topic', ]

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'user' ]

admin.site.register(models.User, UserAdmin)


admin.site.register(models.Tag)
admin.site.register(models.Topic)
admin.site.register(models.Like)
admin.site.register(models.Bookmark, BookmarkAdmin)
admin.site.register(models.Content, ContentAdmin)
admin.site.register(models.Comment, CommentAdmin)