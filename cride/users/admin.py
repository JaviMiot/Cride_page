# * user models admin admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# * models
from cride.users.models import Users, Profiles


class CustomUserAdmin(UserAdmin):
    """Usermodel admin

    Args:
        UserAdmin ([type]): [description]
    """

    list_display = ('email',
                    'username',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'is_cliente')

    list_filter = ('is_cliente', 'is_staff', 'created', 'modified')

@admin.register(Profiles)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('users','reputation', 'rides_taken', 'rides_offered')
    search_fields =('users__username','users__email','users__first_name','users__last_name')
    list_filter = ('reputation',)

admin.site.register(Users, CustomUserAdmin)
