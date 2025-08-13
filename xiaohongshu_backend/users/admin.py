from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    自定义用户后台管理
    """
    # 在后台显示的字段
    list_display = ('username', 'email', 'phone_number', 'nickname', 'is_staff', 'date_joined')

    # UserAdmin.fieldsets 是一个包含多个元组的元组，每个元组代表一个字段集
    # 我们需要将自定义字段添加到 UserAdmin 的 fieldsets 中

    # 复制 UserAdmin 的原始 fieldsets
    fieldsets = list(UserAdmin.fieldsets)

    # 添加我们的自定义字段集
    # ('None', ...) 是一个不带标题的字段集
    # 可以在 'Personal info' 或者其他部分添加
    # 这里我们添加一个新的字段集 "额外信息"
    fieldsets.append(
        ('额外信息', {'fields': ('nickname', 'avatar', 'phone_number', 'bio')})
    )
