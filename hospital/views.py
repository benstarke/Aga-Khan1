
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import *
#from .forms import RegistrationForm

from .forms import *


def index(request):
	return render(request,'hospital/index.html')

def about(request):
	return render(request,'hospital/about.html')


def service(request):
	if request.method == 'POST':
		form = AppointmentForm(request.POST)
		if form.is_valid():
			form.save() # saves in database
			messages.success(request, f"Your appointment has been confirmed.You will get information through email.")
	else:
		form = AppointmentForm()
	return render(request,'hospital/service.html',{'form': form})


'''class RegistrationView(CreateView):
    template_name = 'registration/signup.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url
'''

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if Account.objects.filter(name=name).exists():
                messages.info(request, 'Username has been taken')
                return redirect('signup')
            elif Account.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            else:
                user = Account.objects.create_user(name=name,email=email,password=password1)
                user.save()
                messages.success(request, 'Congrats for signing up!')
                return redirect('signup')
        else:
            messages.info(request, 'password does not match')
            return redirect('signup')

    else:
        return render(request,'registration/signup.html',{'title':'signup'})

def appointment(request):
	if request.method == 'POST':
		form = AppointmentForm(request.POST)
		if form.is_valid():
			form.save() # saves in database
			messages.success(request, f"Your appointment has been confirmed.You will get information through email.")
	else:
		form = AppointmentForm()
	return render(request,'hospital/appointment.html',{'form': form})

