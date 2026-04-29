import requests
import urllib3
from django.shortcuts import render
from django.http import JsonResponse

# SSL ভেরিফিকেশন ওয়ার্নিং বন্ধ করার জন্য
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def image_to_video_view(request):
    if request.method == "POST":
        prompt = request.POST.get('prompt', '')
        mode = request.POST.get('mode', 'text_to_video')

        # আপনার নতুন স্পেসের সঠিক URL (নাম অনুযায়ী আপডেট করা হয়েছে)
        api_url = "https://ziaur07041998-text-to-video.hf.space/generate-video"

        if not prompt:
            return JsonResponse({'status': 'error', 'message': 'Please provide a prompt.'})

        try:
            # ১০ মিনিট (৬০০ সেকেন্ড) সময় এবং SSL ভেরিফিকেশন বন্ধ (verify=False)
            response = requests.post(
                api_url, 
                data={'mode': mode, 'prompt': prompt}, 
                timeout=600,
                verify=False 
            )

            if response.status_code == 200:
                # সফল হলে ভিডিও লিঙ্ক ফেরত পাঠাবে
                return JsonResponse(response.json())
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': f"Server Status: {response.status_code}. Space is still building or starting up."
                })

        except requests.exceptions.Timeout:
            return JsonResponse({'status': 'error', 'message': 'Processing took too long. Please wait a few minutes and try again.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Connection Error: {str(e)}"})

    # GET রিকোয়েস্টে পেজ লোড হবে
    return render(request, 'image_to_video/index.html')