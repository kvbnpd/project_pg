from django.shortcuts import render, redirect
from .forms import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserQueryForm
from .models import UserQuery
from worker.views import workerhome
from agentapp.views import agenthome
from migrantapp.models import Contractor,Migrant
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Login, Contractor, Migrant
from django.urls import reverse
from functools import wraps
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required






# Create your views here.
def index(request):
    return render(request,'index.html')
def userreg(request):
    return render(request,'userregistration.html')
def userhome(request):
    return render(request,'userhome.html')
def footer(request):
    return render(request,'footer.html')

def contact(request):
    return render(request,'contact.html')
def About(request):
    return render(request,'About.html')
def services(request):
    return render(request,'services.html')





def reg(request):
    if request.method == "POST":
        form = ContractorForm(request.POST, request.FILES)
        if form.is_valid():
            # Step 1: Create user in Login table
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            login_user = Login.objects.create(email=email, password=password, user_type="contractor")

            # Step 2: Create contractor profile linked to login
            contractor = form.save(commit=False)
            contractor.login = login_user  # Link to login table
            contractor.save()

            # Step 3: Redirect to login page
            return redirect("login")
        else:
            print(form.errors)
           

    else:
        form = ContractorForm()

    return render(request, "reg.html", {"form": form})

def migrantreg(request):
    if request.method == "POST":
        form = MigrantForm(request.POST, request.FILES)
        if form.is_valid():
            # Step 1: Create user in Login table
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            login_user = Login.objects.create(email=email, password=password, user_type="migrant")

            # Step 2: Create contractor profile linked to login
            contractor = form.save(commit=False)
            contractor.login = login_user  # Link to login table
            contractor.save()

            # Step 3: Redirect to login page
            return redirect("login")
        else:
            print(form.errors)
           

    else:
        form = MigrantForm()

    return render(request, "migrantreg.html", {"form": form})


from django.shortcuts import render, redirect
from .models import Login, Contractor, Migrant
from .forms import loginForm
from functools import wraps
from django.views.decorators.cache import cache_control, never_cache

# -----------------------
# Custom Decorator
# -----------------------
def session_required(user_type=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if 'user_id' not in request.session:
                return redirect('login')
            if user_type and request.session.get('user_type') != user_type:
                return redirect('login')  # or 403 page
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# -----------------------
# Login View
# -----------------------
def login(request):
    if request.method=="GET":
        form=loginForm()
        return render(request,'login.html',{'form':form}) 
    else:
        form=loginForm()    
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        if Login.objects.filter(email=email,password=password).exists():
            print("insiden login exist")
            userdetail=Login.objects.get(email=email,password=password)
            print(userdetail.user_type)
            if(userdetail.user_type=='admin'):
                print("inside admin")
                return render(request, 'admindash.html')
            elif(userdetail.user_type=='police'):
                police_obj = PoliceStations.objects.get(login=userdetail)
                print(police_obj)
                request.session['police_id'] = police_obj.id
                request.session['police_name'] = police_obj.name
                print("inside police")
                return render(request, 'dashboard.html')
            
            elif(userdetail.user_type=='contractor'):
                print("GHf")
                agent_obj = Contractor.objects.get(login=userdetail)
                print(agent_obj)
                request.session['contractor_id'] = agent_obj.id
                request.session['contractor_name'] = agent_obj.name

                return render(request,'agent.html')
            elif(userdetail.user_type=='migrant'):
                worker_obj = Migrant.objects.get(login=userdetail)
                request.session['migrant_id'] = worker_obj.id

                return redirect('workerhome')
            else:
                form=loginForm()  
                return render(request, 'index.html',{'form':form})
        return render(request, 'login.html',{'form':form})


# -----------------------
# Logout View
# -----------------------
@never_cache
def logout(request):
    request.session.flush()
    return redirect('login')

# -----------------------
# Example Protected View
# -----------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@session_required('contractor')
def agenthome(request):
    contractor_id = request.session.get('contractor_id')
    if not contractor_id:
        return redirect('login')

    pending_count = JobBooking.objects.filter(contractor_id=contractor_id, status='Pending').count()
    return render(request, 'agent.html', {'pending_count': pending_count})
# -----------------------
# Migrant Protected View
# -----------------------
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@session_required('migrant')
def workerhome(request):
    migrant_id = request.session.get('migrant_id')
    if not migrant_id:
        return redirect('login')

    # Example data rendering
    return render(request, 'worker/workerhome.html', {
        'migrant_id': migrant_id,
        # Add more context if needed
    })



def contact_admin(request):
    if request.method == 'POST':
        form = UserQueryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the query to the database
            return redirect('success')  # Redirect to the success page after submission
    else:
        form = UserQueryForm()

    # Fetch all user queries to display them
    queries = UserQuery.objects.all()

    return render(request, 'contact_admin.html', {'form': form, 'queries': queries})


#-----------------------------------------------------------------------


def admin_dashboard(request):
    obj=Contractor.objects.all()
    return render(request,'admindash.html')




def registration_choice(request):
    return render(request,'choice.html')

def book_job(request):
    if request.method == "POST":
        form = JobBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect after successful booking
    else:
        form = JobBookingForm()
    
    return render(request, 'bookforajob.html', {'form': form})

def success_view(request):
    return render(request, 'success.html', {'message': 'Job booked successfully!'})






