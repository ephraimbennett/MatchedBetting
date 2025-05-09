from django.contrib import admin
from .models import Member
from django.contrib.auth.admin import UserAdmin
from .forms import MemberCreationForm, MemberChangeForm

# Register your models here.

class MemberAdmin(UserAdmin):
    # Set the forms for a member
    add_form = MemberCreationForm
    form = MemberChangeForm

    # Fields to display in the list view
    list_display = ('email', 'phone', 'is_staff', 'is_superuser')
    
    # Fields to include in the add/edit forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('phone',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),)
    
    # Fields to include in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone', 'is_staff', 'is_superuser'),
        }),
    )
    
    # Ordering for the list view
    ordering = ('email',)

    # Display 'joined_date' as a read-only field
    readonly_fields = ('joined_date',)

admin.site.register(Member, MemberAdmin)