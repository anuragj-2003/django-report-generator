from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from .utils import handle_uploaded_file, generate_summary_excel

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary = handle_uploaded_file(request.FILES['file'])
            request.session['summary'] = summary
            return render(request, 'file_upload/summary.html', {'summary': summary})
    else:
        form = UploadFileForm()
    return render(request, 'file_upload/upload.html', {'form': form})

def export_summary(request):
    summary = request.session.get('summary')
    if summary:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=summary.xlsx'
        generate_summary_excel(summary, response)
        return response
    return HttpResponse("No summary available for export.")
