from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth.admin import UserAdmin  # Base class for user admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
admin.site.register(FlatNumber)
admin.site.register(Visitor)



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUserModel
        fields = ('mobile', 'name', 'email', 'role','flat_no')

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    model = CustomUserModel
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'role', 'flat_no')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'name', 'email', 'role', 'flat_no', 'password1', 'password2')}
        ),
    )

    list_display = ('mobile', 'name', 'email', 'role', 'is_staff')
    search_fields = ('mobile', 'name')
    ordering = ('mobile',)



admin.site.register(CustomUserModel, CustomUserAdmin)