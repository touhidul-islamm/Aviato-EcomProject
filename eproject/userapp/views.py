from django.shortcuts import render, redirect
from . forms import *

# Create your views here.
def registration(request):
    if request.method== 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form=RegistrationForm()
    
    context={
        'form':form
    }

    return render(request, 'userapp/register.html', context)


def profileupdate(request):
    if request.method=='POST':
        u_form=UpdateRegistration(request.POST, instance=request.user)
        p_form=Updateprofile(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('index')
    else:
        u_form=UpdateRegistration(instance=request.user)
        p_form=Updateprofile(request.FILES, instance=request.user.profile)
        context={
            'u_form':u_form,
            'p_form':p_form,
        }
    
    return render(request, 'userapp/profileupdate.html', context)

def profiledetails(request):
    return render(request, 'userapp/profiledetails.html')




