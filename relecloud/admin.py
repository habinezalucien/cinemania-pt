from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserAccount, UserChangeAccount
from .models import User, Movie, Favorite_Movie, watch_list, Comment, Activity

class UserAccountAdmin(UserAdmin):
    add_form = UserAccount
    form = UserChangeAccount
    model = User
    list_display = ['first_name', 'last_name', 'email', 'age', 'gender', 'profile_image', 'username']
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('age', 'gender', 'profile_image')}),)

admin.site.register([Movie, Favorite_Movie, watch_list, Comment, Activity])
admin.site.register(User, UserAccountAdmin)
