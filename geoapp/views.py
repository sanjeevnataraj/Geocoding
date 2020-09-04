from django.shortcuts import render
from geoapp.forms import UploadFileForm
from geoapp.upload_file_helpers import generate_excel_status
from django.conf import settings
from django.http import HttpResponse
import os


# Create your views here.

def upload_file(request):
    context = dict() 
    generate_excel = False
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filename = request.FILES['file']
            generate_excel = generate_excel_status(filename)
            context['file_name'] = filename
    else:
        form = UploadFileForm()    
    context['form'] = form
    context['generate_excel_status'] = generate_excel
    
    return render(request,"upload_file.html",context)

def download_file(request,filename):
    directory =  settings.STATIC_DIR + '/files/'
    file_path = directory + f'{filename}'
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read())
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = 'attachment; filename=report.xlsx'
        return response

    