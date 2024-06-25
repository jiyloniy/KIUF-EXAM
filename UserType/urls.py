# urls rotes for UserType app
from django.urls import path
from UserType.views import UserLoginView,StudentViewSet,FakultetViewSet,TeacherViewSet,UquvBoshqarmasiViewSet

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('student/', StudentViewSet.as_view({'get': 'list', 'post': 'create'}), name='student-list'),
    path('student/<int:pk>/', StudentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy','patch':'partial_update'}), name='student-detail'),
    path('fakultet/', FakultetViewSet.as_view({'get': 'list', 'post': 'create'}), name='fakultet-list'),
    path('fakultet/<int:pk>/', FakultetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy','patch':'partial_update'}), name='fakultet-detail'),
    path('teacher/', TeacherViewSet.as_view({'get': 'list', 'post': 'create'}), name='teacher-list'),
    path('teacher/<int:pk>/', TeacherViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy','patch':'partial_update'}), name='teacher-detail'),
    
    path('uquv-boshqarmasi/<int:pk>/', UquvBoshqarmasiViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch':'partial_update'}),name='uquv-boshqarmasi-detail'),
]

