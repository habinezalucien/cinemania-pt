from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserAccount(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'gender', 'profile_image')
        

class UserChangeAccount(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'gender', 'profile_image')

