from django.shortcuts import render
from django.http import FileResponse
import os
import tempfile
import subprocess
from .forms import WordToPdfForm

def word_to_pdf_view(request):
    if request.method == 'POST':
        form = WordToPdfForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['word_file']
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_in:
                for chunk in uploaded_file.chunks():
                    tmp_in.write(chunk)
                input_path = tmp_in.name

            output_path = input_path.replace('.docx', '.pdf')

            try:
                # LibreOffice দিয়ে কনভার্ট (ফরম্যাটিং + বাংলা + সিম্বল ঠিক থাকবে)
                subprocess.run([
                    'libreoffice', 
                    '--headless', 
                    '--convert-to', 'pdf', 
                    '--outdir', os.path.dirname(output_path),
                    input_path
                ], check=True, timeout=30)

                response = FileResponse(
                    open(output_path, 'rb'),
                    as_attachment=True,
                    filename=uploaded_file.name.replace('.docx', '.pdf')
                )

                # Cleanup
                os.unlink(input_path)
                if os.path.exists(output_path):
                    os.unlink(output_path)

                return response

            except Exception as e:
                if os.path.exists(input_path):
                    os.unlink(input_path)
                return render(request, 'word_to_pdf/index.html', {
                    'form': form,
                    'error': f'কনভার্শন ব্যর্থ: {str(e)}'
                })

    else:
        form = WordToPdfForm()

    return render(request, 'word_to_pdf/index.html', {'form': form})
