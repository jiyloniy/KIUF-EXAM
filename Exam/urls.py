from django.urls import path
from Exam import views
urlpatterns = [
    
    path('TestPageView/', views.TestPageView.as_view({'get': 'list', 'post': 'create'}), name='TestPageView-list'),
    path('TestPageView/<int:pk>/', views.TestPageView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy','patch':'partial_update'}), name='TestPageView-detail'),
    path('Questionsview/', views.Questionsview.as_view({'get': 'list', 'post': 'create'}), name='Questionsview-list'),
    path('Questionsview/<int:pk>/', views.Questionsview.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy','patch':'partial_update'}), name='Questionsview-detail'),
    path('AnswersView/', views.AnswersView.as_view({'get': 'list', 'post': 'create'}), name='AnswersView-list'),
    path('AnswersView/<int:pk>/', views.AnswersView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy','patch':'partial_update'}), name='AnswersView-detail'),
    
    path('TestsView/', views.TestsView.as_view({'get': 'list', 'post': 'create'}), name='TestsView-list'),
    path('TestsView/<int:pk>/', views.TestsView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy','patch':'partial_update'}), name='TestsView-detail'),
   
]
