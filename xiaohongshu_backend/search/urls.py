from django.urls import path
from .views import NoteSearchView, UserSearchView

urlpatterns = [
    path('notes/', NoteSearchView.as_view(), name='search-notes'),
    path('users/', UserSearchView.as_view(), name='search-users'),
]
