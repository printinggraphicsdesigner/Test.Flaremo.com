from django.shortcuts import render
from .models import Tool   # 👈 ADD

def home(request):
    tools = Tool.objects.filter(is_active=True)   # 👈 CHANGE
    return render(request, 'home.html', {'tools': tools})
