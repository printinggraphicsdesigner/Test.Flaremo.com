from django.shortcuts import render

def home(request):
    tools = [
        {
            'name': 'Word to PDF',
            'url': '/word-to-pdf/',
            'description': 'Microsoft Word (.docx) ফাইলকে PDF এ কনভার্ট করুন',
            'icon': '📄'
        },
        # এখানে পরে আরও টুল যোগ করবে
    ]
    return render(request, 'home.html', {'tools': tools})