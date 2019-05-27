from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.admin import UserAdmin
from django import forms

from appGastos.models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Usuarios
        fields = ('nome', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PersonalUserAdmin(UserAdmin):
    fieldsets = ()
    add_fieldsets = (
        (
            None, {'fields': ('email', 'password1', 'password2')}
         ),
    )

    list_display = ('nome', 'email', 'is_superuser', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('nome', 'is_active', 'email')
    ordering = ('nome',)


admin.site.register(Usuarios,  PersonalUserAdmin)
admin.site.register(Categoria)
admin.site.register(Transacao)
