from django.urls import path
from .views import SignUpView,index

urlpatterns = [
    path('', index, name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
    path('create-password/', views.create_password_view, name='create_password'),
    path('add/', views.add_memory_view, name='add_memory'),
    path('stories/', views.view_stories_view, name='view_stories'),
    path('story/<int:pk>/', views.story_detail_view, name='story_detail'),
]