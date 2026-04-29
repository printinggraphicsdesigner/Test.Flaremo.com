from django.shortcuts import render
from django.http import JsonResponse
import cloudinary.uploader
import cloudinary
from gradio_client import Client, handle_file
import os

# Cloudinary Configuration
cloudinary.config(
    cloud_name = "dwxmcdf1u",
    api_key = "739554671348616",
    api_secret = "0Tn3VfQuFaIxbRJYjSOM4L0l750",
    secure = True
)

def ocr_view(request):
    """
    Flaremo Image to Text Converter - Perfect Formatting Version
    """
    if request.method == 'GET':
        return render(request, 'image_to_text/index.html')

    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            
            # ১. ক্লাউডিনারিতে ছবি আপলোড
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result.get('secure_url')
            
            # ২. Hugging Face Space কানেকশন
            client = Client("Ziaur07041998/Image-To-Text-Gradio") 
            
            # ৩. এপিআই কল
            result = client.predict(
                handle_file(image_url)
            )
            
            # --- ফরম্যাটিং ম্যাজিক: লাইন এবং সিম্বল ঠিক রাখা ---
            raw_text = str(result)
            
            # ক) টেক্সটকে লাইনে ভাগ করা
            lines = raw_text.splitlines()
            
            # খ) শুধু সেই লাইনগুলো রাখা যেগুলোতে আসল লেখা আছে (অতিরিক্ত ফাঁকা লাইন বাদ)
            # এটি তারিখের '/' বা স্পেশাল সিম্বলগুলোকে একদম টাচ করবে না
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            
            # গ) লাইনগুলোকে আবার জোড়া লাগানো যেন প্যারাগ্রাফ নষ্ট না হয়
            final_text = "\n".join(cleaned_lines)
            
            # ৪. সফল হলে জেসন রেসপন্স পাঠানো
            return JsonResponse({
                'status': 'success',
                'extracted_text': final_text
            })
            
        except Exception as e:
            print(f"--- DETAILED ERROR LOG START ---")
            print(str(e))
            print("--- DETAILED ERROR LOG END ---")
            
            error_msg = "সার্ভারের সাথে যোগাযোগ করা যাচ্ছে না। হাগিং ফেস স্পেসটি চেক করুন।"
            return JsonResponse({
                'status': 'error', 
                'message': error_msg
            }, status=500)

    return render(request, 'image_to_text/index.html')
