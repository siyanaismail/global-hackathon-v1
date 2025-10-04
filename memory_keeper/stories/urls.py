from django.urls import path
from .views import SignUpView,index

urlpatterns = [
    path('', index, name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
]