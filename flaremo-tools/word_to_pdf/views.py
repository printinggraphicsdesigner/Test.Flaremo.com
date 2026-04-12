from django.shortcuts import render
from django.http import FileResponse
import os
import tempfile
from mammoth import convert_to_html
from xhtml2pdf import pisa
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
                # Convert Word to HTML
                with open(input_path, "rb") as docx_file:
                    result = convert_to_html(docx_file)
                    html_content = result.value

                # Convert HTML to PDF
                with open(output_path, "w+b") as pdf_file:
                    pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
                
                if pisa_status.err:
                    raise Exception("PDF generation failed")

                # Send PDF to user
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
                    'error': f'কনভার্শন ব্যর্থ হয়েছে: {str(e)}'
                })

    else:
        form = WordToPdfForm()

    return render(request, 'word_to_pdf/index.html', {'form': form})
