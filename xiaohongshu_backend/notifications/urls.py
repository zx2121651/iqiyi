from django.urls import path
from .views import NotificationListView, MarkAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('mark-all-as-read/', MarkAsReadView.as_view(), name='notification-mark-all-read'),
    path('<int:pk>/mark-as-read/', MarkAsReadView.as_view(), name='notification-mark-one-read'),
]
