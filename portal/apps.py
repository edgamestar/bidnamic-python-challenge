from django import forms
from django.apps import AppConfig, apps
from django.contrib import admin


class PortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portal'

    def ready(self):
        from portal.models import User
        from django.contrib.auth.admin import UserAdmin

        class UserCreationForm(forms.ModelForm):
            class Meta:
                model = User
                fields = ('username',)

            def save(self, commit=True):
                # Save the provided password in hashed format
                user = super(UserCreationForm, self).save(commit=False)
                user.set_password(self.cleaned_data["password"])
                if commit:
                    user.save()
                return user

        class CustomUserAdmin(UserAdmin):
            # The forms to add and change user instances
            add_form = UserCreationForm
            list_display = (
                "username", "email", "date_joined", "is_active", "last_login",)
            ordering = ("-date_joined",)

            fieldsets = (
                (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'last_login')}),
            )
            add_fieldsets = (
                (None, {
                    'classes': ('wide',),
                    'fields': ('username', 'email', 'password', 'is_superuser', 'is_staff')}
                 ),
            )

            filter_horizontal = ()

        models = apps.get_models()
        for model in models:
            # print(model.__name__)
            # admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
            try:
                # admin.site.register(model, admin_class)
                if model.__name__ == "User":
                    admin.site.register(model, CustomUserAdmin)
                else:
                    admin.site.register(model)
            except admin.sites.AlreadyRegistered:
                pass