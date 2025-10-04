
from django.shortcuts import render 
from .models import Memory # Import Memory model

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

def index(request):
    memories = Memory.objects.all().order_by('-created_at') # Get all memories, newest first
    context = {
        'memories': memories
    }
    return render(request, 'home.html', context)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # Redirect to login page after signup
    template_name = 'signup.html'