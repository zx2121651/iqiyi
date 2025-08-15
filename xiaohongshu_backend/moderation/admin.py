from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    举报后台管理界面
    """
    list_display = ('id', 'reporter_username', 'reported_content_link', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    list_editable = ('status',)
    search_fields = ('reporter__username', 'details')
    readonly_fields = ('reporter', 'content_type', 'object_id', 'reported_content_link', 'created_at', 'updated_at')

    fieldsets = (
        ('举报信息', {
            'fields': ('reporter', 'reported_content_link', 'reason', 'details')
        }),
        ('处理状态', {
            'fields': ('status',)
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def reporter_username(self, obj):
        return obj.reporter.username
    reporter_username.short_description = '举报人'

    def reported_content_link(self, obj):
        if obj.content_object:
            # 获取被举报对象的 admin URL
            admin_url = reverse(
                f'admin:{obj.content_type.app_label}_{obj.content_type.model}_change',
                args=(obj.object_id,)
            )
            return format_html('<a href="{}">{}</a>', admin_url, obj.content_object)
        return "N/A"
    reported_content_link.short_description = '被举报的内容'
    reported_content_link.allow_tags = True
