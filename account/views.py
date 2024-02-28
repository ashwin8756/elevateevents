from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import FormView,CreateView,ListView
from django.urls import reverse_lazy
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"please login!!")
            return redirect('log')
    return inner

dec=[signin_required,never_cache]


# Create your views here.

class LogView(FormView):
    template_name="log.html"
    form_class=LogForm
    def post(self,request):
        form=LogForm(data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                messages.success(request,"Login Successful")
                return redirect('home')
            else:
                messages.error(request,"Invalid Username or Password!!")
                return redirect('log')
        return render(request,"log.html",{"form":form})
    
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('log')
    
class RegView(CreateView):
    template_name="reg.html"
    form_class=RegForm
    model=User
    success_url=reverse_lazy('log')
    def form_valid(self, form):
        messages.success(self.request,"Registration successful")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Validation Failed")
        return super().form_invalid(form)

@method_decorator(dec,name="dispatch")
class HomeView(View):
    def get(self,request):
        return render(request,"home.html")