import requests
import urllib3
from django.shortcuts import render
from django.http import JsonResponse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ocr_view(request):
    if request.method == "POST" and request.FILES.get('image'):
        image_file = request.FILES['image']
        # ইউআরএলটি আপনার স্পেস অনুযায়ী চেক করুন
        api_url = "https://ziaur07041998-image-to-text.hf.space/image-to-text"

        try:
            print(f"Sending image to: {api_url}") # টার্মিনালে দেখাবে
            files = {'image': (image_file.name, image_file.read(), image_file.content_type)}
            
            # টাইমআউট ১৮০ সেকেন্ড করে দেওয়া হয়েছে যাতে বড় ইমেজ প্রসেস হতে পারে
            response = requests.post(api_url, files=files, timeout=180, verify=False)
            
            print(f"Server Status Code: {response.status_code}") # ২০০ না আসলে বুঝবেন সমস্যা আছে
            
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                print(f"Server Response Error: {response.text}")
                return JsonResponse({'status': 'error', 'message': f'Server responded with {response.status_code}'})
                
        except Exception as e:
            print(f"Request Exception: {str(e)}") # কানেকশন এরর হলে এখানে দেখাবে
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'image_to_text/index.html')