from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Memory
from .forms import MemoryForm, SignupForm, LoginForm
from django.http import JsonResponse
import json
from .ai_logic import get_ai_response

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def home_view(request):
    memories = Memory.objects.all().order_by('-created_at')
    context = {'memories': memories}
    return render(request, 'home.html', context)

@login_required
def add_memory_view(request):
    if request.method == 'POST':
        form = MemoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MemoryForm()
    context = {'form': form}
    return render(request, 'add_memory.html', context)

@login_required
def conversation_view(request):
    return render(request, 'conversation.html')

def ai_chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        ai_reply = get_ai_response(user_message)
        return JsonResponse({'reply': ai_reply})