from django.shortcuts import render, redirect
from .models import Memory
from .forms import MemoryForm
from django.http import JsonResponse
import json
from .ai_logic import get_ai_response 

# from django.shortcuts import render 
# from .models import Memory # Import Memory model

# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic

# def index(request):
#     memories = Memory.objects.all().order_by('-created_at') # Get all memories, newest first
#     context = {
#         'memories': memories
#     }
#     return render(request, 'home.html', context)

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login') # Redirect to login page after signup
#     template_name = 'signup.html'





from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse # Required for PDF export
from .models import Memory
from .forms import MemoryForm, LoginForm, SignupForm # Assume these forms exist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# --- Placeholder Authentication Views (MVP friendly) ---

def signup_view(request):
    """Handles user sign-up."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Redirect to the create_password step (or home, depending on your flow)
            return redirect('create_password') 
    else:
        form = SignupForm()
    
    # Renders the signup.html template
    return render(request, 'signup.html', {'form': form})

def create_password_view(request):
    """
    Placeholder view for the two-step signup process.
    In a real app, this would handle activation/setting the password post-signup.
    """
    # Simply redirects to login for the MVP flow simplicity
    if request.method == 'POST':
        # Logic to set the password would go here
        return redirect('login') 
        
    # Renders the create_password.html template
    return render(request, 'create_password.html')


def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Add an error message to the form/context
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    # Renders the login.html template
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """Logs the user out and redirects to the login page."""
    logout(request)
    return redirect('login')


# --- Core Memory Keeper Views ---

@login_required # Ensures only logged-in users can see the homepage
def home_view(request):
    """ This will be your main page, showing all memories. """
    memories = Memory.objects.all().order_by('-created_at')
    context = {'memories': memories}
    return render(request, 'home.html', context)

def add_memory_view(request):
    """ This will handle the form for adding a new memory. """
    if request.method == 'POST':
        form = MemoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') # Redirect to the homepage after saving
    else:
        form = MemoryForm()

    context = {'form': form}
    return render(request, 'add_memory.html', context)

def ai_chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        # Get the real AI response
        ai_reply = get_ai_response(user_message)

        return JsonResponse({'reply': ai_reply})

@login_required
def story_export_view(request, pk):
    """Exports a single memory as a PDF file using xhtml2pdf."""
    
    memory = get_object_or_404(Memory, pk=pk)
    
    # Render a separate clean HTML template optimized for PDF creation
    template_name = 'pdf_template.html'
    context = {'memory': memory}
    
    # RENDER HTML TO PDF LOGIC
    html_content = render(request, template_name, context).content.decode('utf-8')
    response = HttpResponse(content_type='application/pdf')

    # Try to import xhtml2pdf when needed (optional dependency)
    # Import xhtml2pdf at runtime to keep it optional and avoid static import errors
    try:
        import importlib
        xhtml2pdf_mod = importlib.import_module('xhtml2pdf')
        pisa = getattr(xhtml2pdf_mod, 'pisa', None)
        xhtml2pdf_available = pisa is not None
    except Exception:
        xhtml2pdf_available = False

    if not xhtml2pdf_available:
        return HttpResponse('PDF generation is not available because xhtml2pdf is not installed.')

    # Create a safe filename (Memory model may not have a `title` field)
    memory_title = getattr(memory, 'title', f'memory_{memory.pk}')
    response['Content-Disposition'] = f'attachment; filename="{memory_title}_Story.pdf"'

    # Create the PDF
    pisa_status = pisa.CreatePDF(
        html_content, dest=response
    )
    
#     # Renders the signup.html template
#     return render(request, 'signup.html', {'form': form})

# def create_password_view(request):
#     """
#     Placeholder view for the two-step signup process.
#     In a real app, this would handle activation/setting the password post-signup.
#     """
#     # Simply redirects to login for the MVP flow simplicity
#     if request.method == 'POST':
#         # Logic to set the password would go here
#         return redirect('login') 
        
#     # Renders the create_password.html template
#     return render(request, 'create_password.html')


# def login_view(request):
#     """Handles user login."""
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 # Add an error message to the form/context
#                 form.add_error(None, "Invalid username or password.")
#     else:
#         form = LoginForm()

#     # Renders the login.html template
#     return render(request, 'login.html', {'form': form})

# def logout_view(request):
#     """Logs the user out and redirects to the login page."""
#     logout(request)
#     return redirect('login')


# # --- Core Memory Keeper Views ---

# @login_required # Ensures only logged-in users can see the homepage
# def home_view(request):
#     """Renders the main homepage and possibly a list of recent memories."""
#     # Fetch a few recent memories to display on the home page (as seen in home.html)
#     recent_memories = Memory.objects.all().order_by('-created_at')[:3]
    
#     # Renders the home.html template
#     return render(request, 'home.html', {'memories': recent_memories})

# @login_required
# def add_memory_view(request):
#     """Handles adding a new Memory entry."""
#     if request.method == 'POST':
#         # Bind the form to the POST data
#         form = MemoryForm(request.POST)
        
#         if form.is_valid():
#             # Save the new memory object
#             memory = form.save(commit=False)
#             # Optional: Assign the current user as the author/owner
#             # memory.user = request.user 
#             memory.save()
            
#             # Redirect to the stories list/timeline page
#             return redirect('view_stories')
#     else:
#         # Create an empty form for GET requests
#         form = MemoryForm()

#     # Renders the add_memory.html template
#     return render(request, 'add_memory.html', {'form': form})

# @login_required
# def view_stories_view(request):
#     """Retrieves and displays all memories in a timeline format."""
    
#     # Fetch all memories, ordered from newest to oldest (for the timeline effect)
#     memories = Memory.objects.all().order_by('-created_at') 
    
#     # Renders the stories_list.html template (Teammate B's timeline view)
#     return render(request, 'stories_list.html', {'memories': memories})

# @login_required
# def story_detail_view(request, pk):
#     """Displays a single memory by its primary key (pk)."""
    
#     # Use get_object_or_404 for clean error handling if the ID is invalid
#     memory = get_object_or_404(Memory, pk=pk)
    
#     # Renders the story_detail.html template
#     return render(request, 'story_detail.html', {'memory': memory})

# # --- WOW Factor View (Hour 9) ---

# @login_required
# def story_export_view(request, pk):
#     """Exports a single memory as a PDF file using xhtml2pdf."""
    
#     memory = get_object_or_404(Memory, pk=pk)
    
#     # Render a separate clean HTML template optimized for PDF creation
#     template_name = 'pdf_template.html'
#     context = {'memory': memory}
    
#     # RENDER HTML TO PDF LOGIC
#     html_content = render(request, template_name, context).content.decode('utf-8')
#     response = HttpResponse(content_type='application/pdf')
#     # Force download with the story's title as the filename
#     response['Content-Disposition'] = f'attachment; filename="{memory.title}_Story.pdf"'

#     # Create the PDF
#     pisa_status = pisa.CreatePDF(
#        html_content, dest=response
#     )
    
#     # If error during PDF creation, return a simple error response
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html_content + '</pre>')
    
#     return response

# # --- Placeholder Views for Navbar Links ---

# @login_required
# def profile_view(request):
#     """Placeholder for the user profile page."""
#     return render(request, 'profile.html')

# @login_required
# def settings_view(request):
#     """Placeholder for the settings page."""
#     return render(request, 'settings.html')