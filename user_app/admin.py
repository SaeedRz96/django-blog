from django.contrib.admin import register,ModelAdmin
from user_app.models import *


@register(UserToken)
class UserTokenAdmin(ModelAdmin):...
