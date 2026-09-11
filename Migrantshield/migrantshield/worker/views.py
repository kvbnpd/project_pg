from django.shortcuts import render,redirect,get_object_or_404
from migrantapp.models import *
from .models import *
from police.models import *
from worker.models import *
from agentapp.models import *
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from migrantapp.models import Contractor


@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def workerhome(request):
    user_id = request.session.get('migrant_id')
    
    if not user_id:
        return redirect('login')

    try:
        migrant = Migrant.objects.get(id=user_id)
        migrant_name = migrant.full_name  # Get the name of the migrant

        query = request.GET.get('q', '')
        contractors = Contractor.objects.all()

        if query:
            contractors = contractors.filter(
                location__icontains=query
            ) | contractors.filter(
                work_description__icontains=query
            )

        return render(request, 'workerhome.html', {'contractors': contractors, 'migrant_name': migrant_name})

    except Migrant.DoesNotExist:
        return redirect('login')



from django.contrib import messages
from django.shortcuts import redirect
from .models import Application_request

def apply_for_job(request, contractor_id):
    user_id = request.session.get('migrant_id')

    if not user_id:
        messages.error(request, "You must be logged in as a migrant to apply.")
        return redirect('login')  # Update to your login view name

    # Check if the migrant already has an active (pending) application
    has_active_application = Application_request.objects.filter(
        migrant_id=user_id,
        status='pending'
    ).exists()

    if has_active_application:
        messages.warning(request, "You have already applied for a job. Please withdraw your current application before applying to another.")
    else:
        Application_request.objects.create(
            contractor_id=contractor_id,
            migrant_id=user_id,
            status='pending'
        )
        messages.success(request, "Application sent successfully!")
    return redirect('workerhome') 



#check application status
def check_application_status(request):
    user=request.session['migrant_id']
    applications = Application_request.objects.filter(migrant_id=user)  # Get applications of the logged-in user
    return render(request, 'check_status.html', {'applications': applications})
def withdraw_application(request, application_id):
    user=request.session['migrant_id']
    application = get_object_or_404(Application_request, id=application_id, migrant_id=user)
    if application.status == "pending":
        application.delete()
        messages.success(request, "Application withdrawn successfully.")
    else:
        messages.warning(request, "You cannot withdraw an approved/rejected application.")
    return redirect('check_application_status')
# Create your views here.

def myhistory(request):
    user_id = request.session.get('migrant_id')
    
    if not user_id:
        return render(request, 'myhistory.html', {'error': 'User not logged in'})
    
    try:
        migrant = Migrant.objects.get(id=user_id)
        applications = Application_request.objects.filter(migrant=migrant)
        crime_reports = CrimeReport.objects.filter(migrant=migrant)
        noc_applications = NOC_application.objects.filter(migrant=migrant)
        noc_issued = NOC_table.objects.filter(Migrant=migrant)
        work_entries = WorkEntry.objects.filter(migrant=migrant).select_related('jobdetails')
        salary_payments = SalaryPayment.objects.filter(migrant=migrant)
        
        schedule = []
        for work in work_entries:
            schedule.append({
                'job': work.jobdetails.description,
                'venue': work.jobdetails.venue,
                'date': work.date,
                'contractor': work.jobdetails.contractor.name
            })
        
        context = {
            'migrant': migrant,
            'applications': applications,
            'crime_reports': crime_reports,
            'noc_applications': noc_applications,
            'noc_issued': noc_issued,
            'schedule': schedule,
            'salary_payments': salary_payments
        }
        return render(request, 'myhistory.html', context)
    except Migrant.DoesNotExist:
        return render(request, 'myhistory.html', {'error': 'Migrant not found'})    
    


def mywork(request):
    # Get migrant_id from session
    user_id = request.session.get('migrant_id')

    # Check if the user is logged in
    if not user_id:
        return redirect('login')  # Redirect to login if not logged in

    try:
        # Get the migrant object using user_id
        migrant = Migrant.objects.get(id=user_id)

        # Fetch only work entries related to the migrant
        work_entries = WorkEntry.objects.filter(migrant=migrant).select_related('jobdetails')

        # Prepare schedule data
        schedule = []
        for work in work_entries:
            schedule.append({
                'job': work.jobdetails.description,
                'venue': work.jobdetails.venue,
                'date': work.date,
                'contractor': work.jobdetails.contractor.name
            })
        
        # Pass schedule to 'mywork.html'
        return render(request, 'mywork.html', {'schedule': schedule})

    except Migrant.DoesNotExist:
        return render(request, 'mywork.html', {'error': 'Migrant not found'})
    

def myprofile(request):
    user_id = request.session.get('migrant_id')
    
    if not user_id:
        return render(request, 'profile.html', {'error': 'User not logged in'})

    try:
        migrant = Migrant.objects.get(id=user_id)
        
        context = {
            'migrant': migrant,
        }
        return render(request, 'myprofile.html', context)
    
    except Migrant.DoesNotExist:
        return render(request, 'myprofile.html', {'error': 'Migrant not found'})
    
    
def edit_migrant_profile(request):
    user_id = request.session.get('migrant_id')
    if not user_id:
        return redirect('login')  # Redirect if not logged in

    migrant = Migrant.objects.get(id=user_id)

    if request.method == 'POST':
        migrant.full_name = request.POST.get('full_name')
        migrant.phone = request.POST.get('phone')
        migrant.age = request.POST.get('age')
        migrant.state = request.POST.get('state')
        migrant.aadhaar = request.POST.get('aadhaar')

        if 'photo' in request.FILES:
            migrant.photo = request.FILES['photo']
        if 'pcc' in request.FILES:
            migrant.pcc = request.FILES['pcc']

        migrant.save()
        return redirect('myprofile')  # Go back to profile

    return render(request, 'edit_migrant_profile.html', {'migrant': migrant})