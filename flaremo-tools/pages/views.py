from django.shortcuts import render

def about(request):
    request.page_slug = 'about'
    return render(request, 'pages/about.html')

def contact(request):
    request.page_slug = 'contact'
    return render(request, 'pages/contact.html')

def privacy(request):
    request.page_slug = 'privacy'
    return render(request, 'pages/privacy.html')

def terms(request):
    request.page_slug = 'terms'
    return render(request, 'pages/terms.html')

def disclaimer(request):
    request.page_slug = 'disclaimer'
    return render(request, 'pages/disclaimer.html')