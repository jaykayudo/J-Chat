import re
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy

from chat.models import User

# Create your views here.
@login_required(login_url='/chat/login/')
def index(request):
    return render(request, 'chat/index.html')

@login_required(login_url='/chat/login/')
def room(request, room_name):
    return render(request, 'chat/chat.html', {
        'room_name': room_name,
        'username': request.user.username
    })
@login_required(redirect_field_name='/chat/')
def personal(request):
    users = User.objects.all()
    return render(request,'chat/personal_chat.html',{'users':users})
    
@login_required()
def chat(request):
    return render(request,'chat/chat.html')
    
def log_user_out(request):
    logout(request)

class AuthView(FormView):
    form_class = AuthenticationForm
    
    template_name = 'chat/login.html'

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super().form_valid(form)
    def get_success_url(self) -> str:
        return self.request.GET.get('next','/chat/')



class SignUpView(FormView):
    form_class = UserCreationForm
    template_name = 'chat/signup.html'

    def form_valid(self, form):
        obj = form.save()
        login(self.request,obj)
        return super().form_valid(form)
    def get_success_url(self) -> str:
        return self.request.GET.get('next','/chat/')