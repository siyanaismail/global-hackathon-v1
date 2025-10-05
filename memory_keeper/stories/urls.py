from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.home_view, name='home'),
=======
    # Main landing / home
    path('', views.home_view, name='home'),
    # Auth / signup / login flows
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('create-password/', views.create_password_view, name='create_password'),
    # Memory CRUD and listing
>>>>>>> 62fa1b9a2b6ec3a2a00878fd999bbe9282afa545
    path('add/', views.add_memory_view, name='add_memory'),
    path('story/<int:pk>/', views.story_detail_view, name='story_detail'),
    path('story/<int:pk>/export/', views.story_export_view, name='story_export'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
]

# from django.urls import path
# from .views import SignUpView,index

# urlpatterns = [
#     path('', index, name='index'),
#     path('signup/', SignUpView.as_view(), name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('create-password/', views.create_password_view, name='create_password'),
#     path('add/', views.add_memory_view, name='add_memory'),
#     path('stories/', views.view_stories_view, name='view_stories'),
#     path('story/<int:pk>/', views.story_detail_view, name='story_detail'),
# ]