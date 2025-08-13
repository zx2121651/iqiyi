from django.urls import path
from .views import FollowingFeedView, ExploreFeedView

urlpatterns = [
    path('following/', FollowingFeedView.as_view(), name='feed-following'),
    path('explore/', ExploreFeedView.as_view(), name='feed-explore'),
]
