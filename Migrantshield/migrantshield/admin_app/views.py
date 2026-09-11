from django.shortcuts import render,redirect,get_object_or_404
from migrantapp.models import Contractor,Login,Migrant
from django.contrib import messages
from .models import *
from agentapp.models import *
from police.models import CrimeReport
from worker.models import Application_request
from django.shortcuts import render
from agentapp.models import Payment
from django.http import JsonResponse
from agentapp.models import Contractor,WorkEntry, NOC_application
from migrantapp.models import Migrant
from police.models import CrimeReport
from migrantapp.models import UserQuery



# Create your views here.

  # Render the admindash.html template
def worktype(request):
    return render(request, 'worktype.html')
def success(request):
    return render(request, 'success.html')
def adminhome(request):
    return render(request, 'admindash.html')
def view_pending_contractors(request):
    contractors = Contractor.objects.filter(status='Pending')  # Fetch only pending contractors
    return render(request, 'contractors_list.html', {'contractors': contractors})
def view_active_contractors(request):
    contractors = Contractor.objects.filter(status='Active')
    contractors_inactive = Contractor.objects.filter(status='Inactive')  # Fetch only pending contractors
    return render(request, 'Activecontractors_list.html', {'contractors': contractors,'inactive':contractors_inactive})

def approve_contractor(request, contractor_id):
    contractor = Contractor.objects.get(id=contractor_id)
    contractor.status = 'Active'
    contractor.save()
    messages.success(request, "Contractor approved successfully.")
    return redirect('view_pending_contractors')
def revoke_contractor(request, contractor_id):
    contractor = Contractor.objects.get(id=contractor_id)
    contractor.status = 'Inactive'
    contractor.save()
    messages.success(request, "Contractor revoked successfully")
    return redirect('view_active_contractors')

def reject_contractor(request, contractor_id):
    contractor = Contractor.objects.get(id=contractor_id)
    login_entry = contractor.login
    contractor.delete()  # Delete contractor entry
    login_entry.delete()  # Delete login entry
    messages.error(request, "Contractor rejected and removed.")
    return redirect('view_pending_contractors')
def restore_contractor(request, contractor_id):
    contractor = get_object_or_404(Contractor, id=contractor_id)
    contractor.status = 'Active'
    contractor.save()
    return redirect('view_active_contractors')
#typeof work
def view_type_of_work(request):
    if request.method == "POST":
        work_name = request.POST.get("work_name")
        if work_name.strip():
            TypeOfWork.objects.create(name=work_name)
            messages.success(request, "New work type added successfully!")
        else:
            messages.error(request, "Work type cannot be empty.")

    works = TypeOfWork.objects.all()
    return render(request, 'type_of_work_list.html', {'works': works})

def delete_type_of_work(request, work_id):
    work = get_object_or_404(TypeOfWork, id=work_id)
    work.delete()
    messages.success(request, "Type of Work deleted successfully!")
    return redirect('view_type_of_work')  # Redirect back to the list after deletion
def allmigrants(request):
    migrants=Migrant.objects.all()
    return render(request,'allmigrants.html',{'migrants':migrants})
def migrant_detail(request, migrant_id):
    # Fetch the migrant or return 404 if not found.
    migrant = get_object_or_404(Migrant, id=migrant_id)
    
    # Fetch related objects.
    crime_reports = CrimeReport.objects.filter(migrant=migrant)
    application_requests = Application_request.objects.filter(migrant=migrant)
    noc_applications = NOC_application.objects.filter(migrant=migrant)
    noc_tables = NOC_table.objects.filter(Migrant=migrant)
    
    # Note: Payment.migrant_ids is a CSV text field.
    # Using a simple filter to check if the migrant's id (as a string) is in the CSV.
    payments = Payment.objects.filter(migrant_ids__contains=str(migrant.id))
    
    work_entries = WorkEntry.objects.filter(migrant=migrant)
    
    context = {
        'migrant': migrant,
        'crime_reports': crime_reports,
        'application_requests': application_requests,
        'noc_applications': noc_applications,
        'noc_tables': noc_tables,
        'payments': payments,
        'work_entries': work_entries,
    }
    
    return render(request, 'migrant_details.html', context)


def view_payments(request):
    payments = Payment.objects.all()

    for payment in payments:
        payment.migrant_count = len(payment.migrant_ids.split(","))  # Split and count

    return render(request, 'view_payment/view_payments.html', {'payments': payments})

def view_payment_details(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Split migrant_ids and fetch corresponding migrants
    migrant_ids = payment.migrant_ids.split(",")
    migrants = Migrant.objects.filter(id__in=migrant_ids)

    context = {
        "payment": payment,
        "migrants": migrants,
    }
    return render(request, "view_payment/view_payment_details.html", context)



def adminhome(request):
    return render(request, 'adminhome.html')






from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from agentapp.models import Payment, NOC_table
from police.models import CrimeReport
from migrantapp.models import Migrant, Contractor

def get_dashboard_data(request):
    # Calculate the date for 6 months ago
    six_months_ago = datetime.now() - timedelta(days=6 * 30)  # Approximation for 6 months

    # Fetch data for the dashboard
    issued_noc_count = NOC_table.objects.filter(issued_date__gte=six_months_ago).count()  # Filter for last 6 months
    total_migrants = Migrant.objects.count()
    total_contractors = Contractor.objects.count()
    total_payments = Payment.objects.filter(date__gte=six_months_ago).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    reported_cases = CrimeReport.objects.count()

    # Chart 1: NOC Issued Data (Last 6 Months)
    noc_chart_data = (
        NOC_table.objects.filter(issued_date__gte=six_months_ago)  # Filter for last 6 months
        .annotate(month=TruncMonth('issued_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    formatted_noc_chart_data = [
        {"month": entry['month'].strftime('%b %Y'), "count": entry['count']} for entry in noc_chart_data
    ]

    # Chart 2: Payments Data (Last 6 Months)
    payment_chart_data = (
        Payment.objects.filter(date__gte=six_months_ago)  # Filter for last 6 months
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    formatted_payment_chart_data = [
        {"month": entry['month'].strftime('%b %Y'), "total": float(entry['total'])} for entry in payment_chart_data
    ]

    # Prepare the response data
    data = {
        "dashboard_data": {
            "issued_noc": issued_noc_count,
            "total_migrants": total_migrants,
            "total_contractors": total_contractors,
            "payments": float(total_payments),
            "reported_cases": reported_cases,
        },
        "noc_chart_data": formatted_noc_chart_data,
        "payment_chart_data": formatted_payment_chart_data,
    }

    return JsonResponse(data)




def view_crime_reports(request):
    # Fetch all crime reports
    crime_reports = CrimeReport.objects.select_related('migrant').all()

    # Add migrant name and reported_date to the context
    context = {
        "crime_reports": [
            {
                "id": report.id,
                "migrant": {
                    "id": report.migrant.id if report.migrant else None,
                },
                "reported_by": report.reported_by,
                "date": report.date_reported,
                "description": report.description,
                "status": report.status,
            }
            for report in crime_reports
        ],
    }
    return render(request, "admin_app/view_crime_reports.html", context)


from agentapp.models import Payment

def views(request):
    payments = Payment.objects.all().order_by('-date')
    return render(request, 'views.html', {'payments': payments})

def view_user_queries(request):
    user_queries = UserQuery.objects.all().order_by('-created_at')
    return render(request, 'view_user_queries.html', {'user_queries': user_queries})






from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from migrantapp.models import UserQuery  # Replace with your model name
from .forms import RespondQueryForm  # We'll make this next

def respond_query(request, query_id):
    query = get_object_or_404(UserQuery, id=query_id)

    if request.method == 'POST':
        form = RespondQueryForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['response']
            send_mail(
                f"Response to your query: {query.subject}",
                message,
                'admin@SafeHorizonNetwork.com',
                [query.email],
                fail_silently=False,
            )
            return redirect('view_user_queries')
    else:
        form = RespondQueryForm()

    return render(request, 'respond_query.html', {'query': query, 'form': form})


from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from migrantapp.models import PoliceStations

def add_police_station(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        location = request.POST.get('location', '').strip()
        district = request.POST.get('district', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Basic empty field validation
        if not all([name, location, district, email, password]):
            messages.error(request, "All fields are required.")
        else:
            # Email validation
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Enter a valid email address.")
                return render(request, 'add_police_station.html', {'stations': PoliceStations.objects.all()})

            if Login.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                login = Login.objects.create(email=email, password=password, user_type="police")
                PoliceStations.objects.create(
                    login=login,
                    name=name,
                    location=location,
                    district=district
                )
                messages.success(request, "Police station added successfully.")

    stations = PoliceStations.objects.all()
    return render(request, 'add_police_station.html', {'stations': stations})

def edit_police_station(request, id):
    station = PoliceStations.objects.get(id=id)
    if request.method == 'POST':
        station.name = request.POST.get('name')
        station.location = request.POST.get('location')
        station.district = request.POST.get('district')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Login.objects.filter(email=email).exclude(id=station.login.id).exists():
            messages.error(request, "Email already exists.")
        else:
            station.login.email = email
            station.login.password = password
            station.login.save()
            station.save()
            messages.success(request, "Police station updated successfully.")
            return redirect('add_police_station')
    return render(request, 'edit_police_station.html', {'station': station})

def delete_police_station(request, id):
    station = PoliceStations.objects.get(id=id)
    station.login.delete()  # Delete associated login
    station.delete()
    messages.success(request, "Police station deleted successfully.")
    return redirect('add_police_station')