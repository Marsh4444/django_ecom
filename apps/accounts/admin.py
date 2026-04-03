from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

@admin.register(Account)
class AccountAdmin(UserAdmin):
     # <-- THIS is the line responsible
    # By extending UserAdmin, you inherit its internal get_form() logic
    # which automatically swaps the password field for a
    # ReadOnlyPasswordHashField widget. You didn't write that logic —
    # it lives inside Django's source code for UserAdmin.
    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_admin')
    list_display_links = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        ('Login Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff')}),
        ('Activity', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    # Override these to clear out UserAdmin's defaults
    # which reference groups/user_permissions/is_superuser
    filter_horizontal = ()   # <-- removes groups & user_permissions references
    list_filter = ('is_admin', 'is_active', 'is_staff')  # <-- only fields that exist on YOUR model
    ordering = ('-date_joined',)