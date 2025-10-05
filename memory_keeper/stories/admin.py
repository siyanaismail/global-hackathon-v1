from django.contrib import admin
from .models import Memory


admin.site.register(Memory) # <-- Tell the admin to manage the model

