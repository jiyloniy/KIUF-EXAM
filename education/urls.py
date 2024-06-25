# urls 
from django.urls import path
from education.views import GroupViewSet, SubjectViewSet

urlpatterns = [
    path('group/', GroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='group-list'),
    path("group/<int:pk>/", GroupViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}), name='group-detail'),
    path('subject/', SubjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='subject-list'),
    path("subject/<int:pk>/", SubjectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}), name='subject-detail'),
    
]