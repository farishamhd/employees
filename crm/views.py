from django.shortcuts import render,redirect
from django.views.generic import View
from crm.forms import EmployeeForm,EmployeesModelForm,RegistratonForm,LoginForm
from crm.models import Employees
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


# Create your views here.
@method_decorator(signin_required,name="dispatch")
class EmployeeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=EmployeesModelForm()
        return render(request,"emp_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=EmployeesModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Added successfully")

            # Employees.objects.create(**form.cleaned_data)
            print("created")
            return render(request,"emp_add.html",{"form":form})
        else:
            messages.error(request,"Failed to add employee")
            return render(request,"emp_add.html",{"form":form})
        
@method_decorator(signin_required,name="dispatch")
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):        
            qs=Employees.objects.all()
            departments=Employees.objects.all().values_list("department",flat=True).distinct()
            print(departments)
            if "department" in request.GET:
                dept=request.GET.get("department")
                qs=qs.filter(department__iexact=dept)
            return render(request,"emp_list.html",{"data":qs,"departments":departments})
        
        

    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Employees.objects.filter(name__icontains=name)
        return render(request,"emp_list.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render(request,"emp_detail.html",{"data":qs})

@method_decorator(signin_required,name="dispatch")   
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        messages.success(request,"Deleted ")
        return redirect("emp-all")

@method_decorator(signin_required,name="dispatch")    
class EmployeeUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeesModelForm(instance=obj)
        return render(request,"emp_edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeesModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"updated")
            return redirect("emp-detail",pk=id)
        else:
            messages.error(request,"failed to update")
            return render(request,"emp_edit.html",{"form":form})
        
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistratonForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistratonForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"created")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"failed")
            return render(request,"register.html",{"form":form})
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            print(request.user,"before")
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            
            user_obj=authenticate(request,username=u_name,password=pwd)
            if user_obj:
                print("valid ")
                login(request,user_obj)
                print(request.user,"after")
                return redirect("emp-all")
        messages.error(request,"inavlid credential")
        return render(request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")   
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

        








