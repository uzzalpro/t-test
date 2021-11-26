# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from testing.models import Document
from testing.forms import DocumentForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    documents = Document.objects.all()
    return render(request, 'testing/home.html', { 'documents': documents })   


def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return render(request,'accounts/index.html')
    context['form']=form
    return render(request,'registration/sign_up.html',context)



def simple_upload(request): # id
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # current_user = request.user
        # user_id = current_user.id        
        return render(request, 'testing/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'testing/simple_upload.html')


def model_form_upload(request):  #id
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'testing/model_form_upload.html', {
        'form': form
    })
    
