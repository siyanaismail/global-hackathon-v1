from django.urls import path
from .views import home_view, add_memory_view, signup_view, login_view, logout_view, ai_chat_api, conversation_view

urlpatterns = [
    path('', home_view, name='home'),
    path('add/', add_memory_view, name='add_memory'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/chat/', ai_chat_api, name='ai_chat_api'),
    path('conversation/', conversation_view, name='conversation'),

]