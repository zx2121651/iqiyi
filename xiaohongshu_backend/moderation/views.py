from rest_framework import generics, permissions
from .models import Report
from .serializers import ReportSerializer

class ReportCreateView(generics.CreateAPIView):
    """
    创建一条新的内容举报
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
