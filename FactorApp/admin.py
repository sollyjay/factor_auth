from FactorApp.models import Follow, Following, User, Post
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
admin.site.unregister(Group)

admin.site.register(Follow)
admin.site.register(Following)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "created_date"]
    ordering = ["-created_date"]
    list_filter = ["text","user"]

"""
class FolloweeInline(admin.TabularInline):
    model = Follow
    fk_name = 'from_user'


class FollowerInline(admin.TabularInline):
    model = Follow
    fk_name = 'to_user'
"""



@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','gender','contact','dob','avatar',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    # inlines = [FolloweeInline, FollowerInline]
    list_display = ('id','email','username','first_name', 'last_name', 'is_staff','gender','contact','dob',)
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('id',)

