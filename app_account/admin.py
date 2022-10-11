from django.contrib import admin
from .models import MyUser, Roles, UserRoles, SecModules, SecRoleModules, LoginHistory

admin.site.register(MyUser)
admin.site.register(Roles)
admin.site.register(UserRoles)
admin.site.register(SecModules)
admin.site.register(SecRoleModules)
admin.site.register(LoginHistory)

# Register your models here.
