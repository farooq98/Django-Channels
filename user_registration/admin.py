from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from core.custom_admin import custom_admin_site
from .models import UserModel
import re

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('name', 'email', 'username', 'date_of_birth', 'image_url')

    def clean_password(self):
        passwd = len(self.cleaned_data['password'])
        if passwd and passwd < 8:
            raise ValidationError("Password must be greater than 8 characters")
        return str(self.cleaned_data['password'])

    def clean_name(self):
        if self.cleaned_data['name']:
            if not bool(re.match('^[a-zA-Z ]+$', self.cleaned_data['name'])):
                raise ValidationError("Name must only contain characters A to Z or a-z")
            else:
                return self.cleaned_data['name']
        return ""

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserModel
        fields = ('name', 'email', 'password', 'image_url', 'date_of_birth', 'is_active', 'is_admin', 'groups', 'user_permissions')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'date_of_birth', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('is_admin',)
    filter_horizontal = ('groups',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('name', 'image_url', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Groups', {'fields': ('groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        ('Register New User', {
            'classes': ('wide',),
            'fields': ('name', 'email', 'username', 'password', 'date_of_birth'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

class UserAdminView(admin.ModelAdmin):

    list_display = ('email', 'is_active', 'is_admin')


admin.site.register(UserModel, UserAdmin)
custom_admin_site.register(UserModel, UserAdminView)

