from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    """
    举报序列化器
    """
    # 让客户端可以通过 app_label 和 model 来指定 content_type
    # 例如: {"content_type_model": "notes.note", "object_id": 1, ...}
    content_type_model = serializers.CharField(write_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'content_type_model', 'object_id', 'reason', 'details',
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate(self, data):
        # 验证 content_type_model
        try:
            app_label, model = data['content_type_model'].split('.')
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        except (ContentType.DoesNotExist, ValueError):
            raise serializers.ValidationError("无效的内容类型。格式应为 'app_label.model'。")

        # 验证 object_id
        if not content_type.model_class().objects.filter(pk=data['object_id']).exists():
            raise serializers.ValidationError("被举报的对象不存在。")

        # 检查是否重复举报
        reporter = self.context['request'].user
        if Report.objects.filter(reporter=reporter, content_type=content_type, object_id=data['object_id']).exists():
            raise serializers.ValidationError("你已经举报过此内容。")

        data['content_type'] = content_type
        return data

    def create(self, validated_data):
        # 移除辅助字段
        validated_data.pop('content_type_model')
        # 添加举报人
        validated_data['reporter'] = self.context['request'].user
        return Report.objects.create(**validated_data)
