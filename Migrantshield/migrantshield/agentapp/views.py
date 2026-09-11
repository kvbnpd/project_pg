from django.shortcuts import render
from django.shortcuts import *
from worker.models import Application_request
from .models import *
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.contrib import messages
import datetime
from .forms import *
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from django.http import JsonResponse
from migrantapp.models import Contractor,JobBooking
from django.http import FileResponse, Http404
import os
from django.conf import settings
from reportlab.lib.pagesizes import mm
from reportlab.lib.pagesizes import landscape, A6 
from django.views.decorators.csrf import csrf_exempt
from worker.models import Application_request
from collections import defaultdict
from django.db.models import Count
from django.utils.timezone import now
from datetime import datetime, date
from django.db.models import Q
from calendar import monthrange
from django.shortcuts import render
from django.db.models import Sum
from .models import SalaryPayment
from datetime import datetime
import datetime as dt
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .models import Migrant, NOC_application




#ID_CARD_SIZE = (85.6 * mm, 54 * mm)  # Standard ID card size in mm


# Create your views here.
def agenthome(request):
    contractor_id= request.session['contractor_id'] 
    pending_count = JobBooking.objects.filter(contractor_id=contractor_id, status='Pending').count()
    
    return render(request, 'agent.html', {'pending_count': pending_count})

    #return render(request,'agent.html')
def view_applications(request):
    contractor = request.session['contractor_id']  # Assuming the contractor is linked to the user
    applications = Application_request.objects.filter(contractor=contractor)

    return render(request, 'my_applications.html', {'applications': applications})
def view_new_applications(request):
    contractor_id = request.session.get('contractor_id')  # Get contractor ID from session
    
    if not contractor_id:
        return redirect('login')  # Redirect if no contractor is logged in

    # Get all migrants who have applied for NOC
    migrants_with_noc = NOC_application.objects.values_list('migrant', flat=True)
    
    # Fetch applications where the migrant is NOT in the NOC_application table
    applications = Application_request.objects.filter(contractor_id=contractor_id).exclude(migrant__in=migrants_with_noc)

    return render(request, 'new_applicants.html', {'applications': applications})


def update_application_status(request, app_id, status):
    application = Application_request.objects.get(id=app_id)
    if status in ['approved', 'rejected']:
        application.status = status
        application.save()
    return redirect('view_applications')



def apply_noc_all(request):
    if request.method == "POST":
        migrant_ids = request.POST.get("migrant_ids", "").split(",")

        if not migrant_ids or migrant_ids == [""]:
            return HttpResponse("No applications selected.", status=400)

        total_amount = len(migrant_ids) * 610

        # Save applications & payment details
        for migrant_id in migrant_ids:
            try:
                migrant = Migrant.objects.get(id=migrant_id)
                NOC_application.objects.create(migrant=migrant, status="Applied")
            except Migrant.DoesNotExist:
                continue  # Skip invalid IDs

        # Save payment to Payment model
        payment_record = Payment.objects.create(
            amount=total_amount,
            migrant_ids=",".join(migrant_ids)  # Store migrant IDs as CSV
        )
        payment_record.save()

        # Generate PDF receipt
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="NOC_Receipt.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # Add Government Logo (Optional)
        try:
            logo = ImageReader("static/images/gov_logo.png")
            pdf.drawImage(logo, 50, height - 80, width=60, height=60, mask="auto")
        except Exception as e:
            print(f"Logo not found: {e}")

        # Kerala Govt Header
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(width / 2, height - 50, "Government of Kerala")
        pdf.setFont("Helvetica", 12)
        pdf.drawCentredString(width / 2, height - 70, "No Objection Certificate (NOC) Payment Receipt")
        pdf.line(50, height - 80, width - 50, height - 80)

        # Receipt details
        pdf.setFont("Helvetica", 11)
        pdf.drawString(50, height - 110, f"Receipt No: NOC-{payment_record.id}")
        pdf.drawString(50, height - 130, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        pdf.drawString(50, height - 150, f"Total Amount Paid: ₹{total_amount}")
        pdf.drawString(50, height - 170, f"Applications Count: {len(migrant_ids)}")

        # List of applicants - Table format
        y_position = height - 210
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(50, y_position, "S.No")
        pdf.drawString(100, y_position, "Applicant Name")
        pdf.drawString(300, y_position, "Age")
        pdf.drawString(350, y_position, "Phone")
        pdf.line(50, y_position - 5, width - 50, y_position - 5)

        pdf.setFont("Helvetica", 11)
        y_position -= 25
        for i, migrant_id in enumerate(migrant_ids, start=1):
            try:
                migrant = Migrant.objects.get(id=migrant_id)
                pdf.drawString(50, y_position, f"{i}.")
                pdf.drawString(100, y_position, migrant.full_name)
                pdf.drawString(300, y_position, str(migrant.age))
                pdf.drawString(350, y_position, migrant.phone)
                y_position -= 20

                # Check if content is going off the page
                if y_position < 100:
                    pdf.showPage()  # Create a new page if the current one is full
                    y_position = height - 50  # Reset the position for the new page

            except Migrant.DoesNotExist:
                continue  # Skip invalid migrant IDs

        # Signature section
        pdf.line(50, y_position - 30, width - 50, y_position - 30)
        pdf.drawString(50, y_position - 50, "Authorized Officer")
        pdf.drawString(50, y_position - 70, "Government of Kerala")

        # Finalize and save PDF
        pdf.showPage()
        pdf.save()

        return response

    return redirect("noc_application_page")

    
def noc_status_page(request):
    contractor_instance = Contractor.objects.get(id=request.session['contractor_id'])

    applns = NOC_application.objects.filter(
        migrant__application_request__contractor=contractor_instance
    ).values('id', 'migrant_id', 'migrant__full_name', 'status', 'applied_date')

    # Remove duplicates manually using set()
    seen_migrants = set()
    unique_applns = []

    for appln in applns:
        if appln['migrant_id'] not in seen_migrants:
            seen_migrants.add(appln['migrant_id'])
            unique_applns.append(appln)

    return render(request, "noc_status.html", {'applications': unique_applns})

def get_noc_status(request):
    search_id = request.GET.get("search_id", "").strip()
    
    if not search_id:
        return JsonResponse({"error": "Invalid ID"}, status=400)

    try:
        noc = NOC_application.objects.get(id=search_id)
        data = {
            "id": noc.id,
            "name": noc.migrant.full_name,
            "status": noc.status,
            "applied": noc.applied_date.strftime("%Y-%m-%d"),
            "approved": noc.approval_date.strftime("%Y-%m-%d") if noc.approval_date else "N/A"
        }
        return JsonResponse(data)
    except NOC_application.DoesNotExist:
        return JsonResponse({"error": "No record found"}, status=404)

def download_noc(request, migrant_id):
    print(f"Requested Migrant ID: {migrant_id}")

    # ✅ Correct query to get the latest NOC for the correct migrant
    noc_entry = get_object_or_404(NOC_table, Migrant__id=migrant_id)

    # ✅ Print file path to verify
    print("Stored file path:", noc_entry.noc.path)

    file_path = noc_entry.noc.path  # Extract the correct file path

    # ✅ Check if the file exists before trying to open it
    if not os.path.exists(file_path):
        print("File does not exist:", file_path)
        return HttpResponse("File not found.", status=404)

    # ✅ Open and send the correct file
    with open(file_path, "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="NOC_{migrant_id}.pdf"'
        return response


    
    
    
def myworkers(request):
    contractor_id = request.session.get('contractor_id')  # Get logged-in contractor ID
    
    if contractor_id:
        # Get NOC-approved migrants
        approved_migrants = NOC_application.objects.filter(status="Approved").values_list('migrant_id', flat=True)
        
        # Get migrants requested by the logged-in contractor, excluding revoked ones
        migrant_list = Migrant.objects.filter(
            application_request__contractor_id=contractor_id,
            application_request__status__in=["approved"],  # Exclude revoked
            id__in=approved_migrants
        ).distinct()

    else:
        migrant_list = []

    return render(request, 'myworkers.html', {'migrants': migrant_list})


def download_idcard(request):
    contractor_id = request.session.get('contractor_id')  # Get logged-in contractor ID
    
    if contractor_id:
        # Get NOC-approved migrants
        approved_migrants = NOC_application.objects.filter(status="Approved").values_list('migrant_id', flat=True)
        
        # Get migrants requested by the logged-in contractor
        migrant_list = Migrant.objects.filter(application_request__contractor_id=contractor_id, id__in=approved_migrants).distinct()

    else:
        migrant_list = []

    return render(request, 'idcard.html', {'migrants': migrant_list})
ID_CARD_WIDTH = 85.6 * mm
ID_CARD_HEIGHT = 54 * mm

def download_id_card_individual(request, migrant_id):
    migrant = get_object_or_404(Migrant, id=migrant_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ID_Card_{migrant.full_name}.pdf"'

    width, height = landscape(A6)  # Landscape A6 for better width
    p = canvas.Canvas(response, pagesize=(width, height))

    # **Draw Border**
    p.setStrokeColorRGB(0, 0, 0)  # Black border
    p.setLineWidth(2)
    p.rect(10, 10, width - 20, height - 20)

    # **Header**
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, height - 30, "Government of India")
    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2, height - 45, "Migrant Worker ID Card")

    # **Unique ID (UMIN + 12 digits)**
    unique_id = f"UMIN{migrant.id:012d}"

    # **Migrant Details**
    p.setFont("Helvetica", 10)
    p.drawString(20, height - 70, f"Full Name: {migrant.full_name}")
    p.drawString(20, height - 90, f"Age: {migrant.age}")
    p.drawString(20, height - 110, f"Unique ID: {unique_id}")
    p.drawString(20, height - 130, "Nationality: Indian")

    # **Migrant Photo**
    if migrant.photo:
        try:
            img = ImageReader(migrant.photo.path)
            p.drawImage(img, width - 90, height - 140, 60, 70, mask='auto')  # Place photo on right side
        except Exception as e:
            print(f"Error loading photo: {e}")

    p.showPage()
    p.save()
    return response


def myjobdetails(request):
    return render(request,'my_jobdetails.html')

def work_entry_view(request):
    if request.method == 'POST':
        form = WorkEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('work_entry')
    else:
        form = WorkEntryForm()

    work_entries = WorkEntry.objects.all().order_by('-date')
    return render(request, 'work_entry.html', {'form': form, 'work_entries': work_entries})

def job_details_view(request):
    contractor_id = request.session.get('contractor_id')  # Assuming session stores contractor ID
    if request.method == 'POST':
        form = JobDetailsForm(request.POST)
        if form.is_valid():
            job_detail = form.save(commit=False)
            job_detail.contractor_id = contractor_id
            job_detail.save()
            return redirect('job_details_view')

    else:
        form = JobDetailsForm()

    job_entries = JobDetails.objects.filter(contractor_id=contractor_id).order_by('-startdate')
    return render(request, 'my_jobdetails.html', {'form': form, 'job_entries': job_entries})

def delete_job_detail(request, job_id):
    job_detail = get_object_or_404(JobDetails, id=job_id)
    job_detail.delete()
    return redirect('job_details_view')

def schedule(request):
    return render(request,'schedule.html')
def get_job_details(request):
    contractor_id = request.session.get('contractor_id') 
    jobs = JobDetails.objects.filter(
    contractor_id=contractor_id
).filter(
    Q(status="Open") | Q(status="Accepted")
).values('id', 'venue')
    return JsonResponse(list(jobs), safe=False)

# def get_migrants(request):
#     contractor_id = request.session.get('contractor_id')

#     if not contractor_id:
#         return JsonResponse({"error": "Contractor ID not found in session"}, status=400)

#     migrants = Application_request.objects.filter(
#         contractor__id=contractor_id, status="approved"
#     ).values('migrant__id', 'migrant__full_name')

#     return JsonResponse(list(migrants), safe=False)


from django.http import JsonResponse

def get_migrants(request):
    contractor_id = request.session.get('contractor_id')
    date = request.GET.get('date')  # Get date from request

    if not contractor_id:
        return JsonResponse({"error": "Contractor ID not found in session"}, status=400)

    # Get approved migrants for the contractor
    approved_migrants = list(Application_request.objects.filter(
        contractor__id=contractor_id, status="approved"
    ).values('migrant__id', 'migrant__full_name'))

    migrant_ids = [m['migrant__id'] for m in approved_migrants]  # Extract migrant IDs

    # Get migrants who already have a work entry on the given date
    assigned_migrants = set(WorkEntry.objects.filter(date=date, migrant_id__in=migrant_ids).values_list('migrant_id', flat=True))

    # Separate available and excluded migrants
    available_migrants = [m for m in approved_migrants if m['migrant__id'] not in assigned_migrants]
    excluded_migrants = [m for m in approved_migrants if m['migrant__id'] in assigned_migrants]

    return JsonResponse({
        "available_migrants": available_migrants,
        "excluded_migrants": excluded_migrants
    }, safe=False)

@csrf_exempt

def save_work_entry(request):
    if request.method == 'POST':
        data = request.POST
        job_id = data.get('jobdetails')
        date = data.get('date')
        migrant_ids = request.POST.getlist('migrants')
        
        print(f"Received Data: {data}")  # ✅ Debug: Check incoming data
        print(f"Selected Job ID: {job_id}, Date: {date}, Migrant IDs: {migrant_ids}")  # ✅ Debug

        duplicate_migrants = []

        for migrant_id in migrant_ids:
            # Check if the migrant already has a work entry on the same date and job
            if WorkEntry.objects.filter(migrant_id=migrant_id, date=date, jobdetails_id=job_id).exists():
                duplicate_migrants.append(migrant_id)
                print(f"Duplicate Entry Found for Migrant {migrant_id} on {date}")  # ✅ Debug
            else:
                # Create a new work entry if no duplicate is found
                WorkEntry.objects.create(migrant_id=migrant_id, jobdetails_id=job_id, date=date)
                print(f"Work Entry Created for Migrant {migrant_id} on {date}")  # ✅ Debug

        # Handle duplicates
        if duplicate_migrants:
            return JsonResponse({
                'message': 'Some migrants already have a work entry on this date.',
                'duplicates': duplicate_migrants
            }, status=400)

        return JsonResponse({'message': 'Work entry saved successfully!'})

    return JsonResponse({'error': 'Invalid request method!'}, status=405)


def view_schedule(request, job_id):
    job = get_object_or_404(JobDetails, id=job_id)
    work_entries = WorkEntry.objects.filter(jobdetails=job).select_related('migrant').order_by('date')

    # Grouping work entries by date
    work_schedule = defaultdict(list)
    for entry in work_entries:
        work_schedule[entry.date].append(entry.migrant.full_name)

    return render(request, 'view_job_schedule.html', {'job': job, 'work_schedule': dict(work_schedule)})

def paysalary(request):
    return render(request,'paysalary.html')


def select_month(request):
    """Page to select the month and year"""
    return render(request, 'select_month.html')

def pay_salary(request):
    """Fetch and display migrants and work details for the selected month"""
    if request.method == "POST":
        selected_month = request.POST.get("month")
        selected_year = request.POST.get("year")
        contractor_id = request.session.get('contractor_id')  # Check if contractor is logged in

        if not selected_month or not selected_year:
            messages.error(request, "Month and year are required!")
            return redirect('select_month')

        try:
            selected_month = int(selected_month)
            selected_year = int(selected_year)
        except ValueError:
            messages.error(request, "Invalid month or year format!")
            return redirect('select_month')

        # Fetch migrant work details under the contractor for the selected month
        work_entries = WorkEntry.objects.filter(
            jobdetails__contractor_id=contractor_id,
            date__month=selected_month,
            date__year=selected_year
        ).values('migrant').annotate(total_days=Count('migrant'))

        migrants_data = []
        for entry in work_entries:
            migrant = get_object_or_404(Migrant, id=entry['migrant'])
            total_salary = entry['total_days'] * 1000  # 1000 per day

            migrants_data.append({
                'migrant': migrant,
                'total_days': entry['total_days'],
                'salary': total_salary
            })

        return render(request, 'pay_salary.html', {
            'migrants_data': migrants_data,
            'month': selected_month,
            'year': selected_year
        })

    return redirect('select_month')


def confirm_payment(request):
    """Confirm and save salary payment details with validation"""
    if request.method == "POST":
        selected_month = request.POST.get("month")
        selected_year = request.POST.get("year")
        contractor_id = request.session.get('contractor_id')  # Ensure contractor is logged in

        if not selected_month or not selected_year:
            messages.error(request, "Month and year are required!")
            return redirect('pay_salary')

        try:
            selected_month = int(selected_month)
            selected_year = int(selected_year)
        except ValueError:
            messages.error(request, "Invalid month or year format!")
            return redirect('pay_salary')

        # Ensure salary is paid only after the last day of the selected month
        today = datetime.now().date()
        last_day_of_selected_month = date(selected_year, selected_month, monthrange(selected_year, selected_month)[1])

        if today <= last_day_of_selected_month:
            messages.error(request, "Salary can only be paid after the end of the selected month.")
            return redirect('pay_salary')

        # Iterate through submitted migrant salary data
        for key, value in request.POST.items():
            if key.startswith("migrant_"):  # Format: migrant_<id>
                migrant_id = key.split("_")[1]
                total_days = request.POST.get(f"days_{migrant_id}")
                salary_amount = request.POST.get(f"salary_{migrant_id}")

                if not total_days or not salary_amount:
                    messages.error(request, "Days worked and salary amount are required!")
                    return redirect('pay_salary')

                try:
                    total_days = int(total_days)
                    salary_amount = float(salary_amount)
                except ValueError:
                    messages.error(request, "Invalid format for days or salary!")
                    return redirect('pay_salary')

                migrant = get_object_or_404(Migrant, id=migrant_id)

                # Check if salary already exists for this migrant in the same month and year
                if SalaryPayment.objects.filter(
                    migrant=migrant, month=selected_month, year=selected_year
                ).exists():
                    messages.error(request, f"Salary for {migrant.full_name} has already been paid for {selected_month}/{selected_year}.")
                    continue

                # Save salary payment record
                SalaryPayment.objects.create(
                    migrant=migrant,
                    contractor_id=contractor_id,
                    month=selected_month,
                    year=selected_year,
                    total_days=total_days,
                    salary_amount=salary_amount
                )

        messages.success(request, "Salary paid successfully!")
        return redirect('select_month')

    return redirect('pay_salary')

def remove_migrant(request):
    if request.method == "POST":
        migrant_id = request.POST.get("migrant_id")
        
        try:
            # Find the application entry
            application = Application_request.objects.get(migrant_id=migrant_id, status="approved")
            
            # Update the status to revoked
            application.status = "revoked"
            application.save()

            return JsonResponse({"success": True})
        except Application_request.DoesNotExist:
            return JsonResponse({"success": False, "message": "Migrant not found or already removed."})
    return JsonResponse({"success": False, "message": "Invalid request."})


def job_requests(request):
    contractor_id = request.session.get('contractor_id')
    pending_jobs = JobBooking.objects.filter(contractor_id=contractor_id, status='Pending')
    
    return render(request, 'job_requests.html', {'pending_jobs': pending_jobs})

def accept_job(request, job_id):
    job = get_object_or_404(JobBooking, id=job_id)

    # Update JobBooking status to 'Accepted'
    job.status = "Accepted"
    job.save()

    # Create a JobDetails entry
    JobDetails.objects.create(
        contractor=job.contractor,
        startdate=job.booked_for,
        description=job.job_description,
        venue=job.location,
    )

    return redirect("job_requests") 

def mark_job_completed(request, job_id):
    job_detail = get_object_or_404(JobDetails, id=job_id)
    job_detail.status="Completed"
    job_detail.save()
    return redirect('job_details_view')

@csrf_exempt
@csrf_exempt
def update_worker_status(request):
    if request.method == 'POST':
        migrant_id = request.POST.get('migrant_id')
        try:
            migrant = Migrant.objects.get(id=migrant_id)

            if migrant.status == 'Active':
                migrant.status = 'Inactive'
                print(f"Migrant {migrant.full_name} is now Inactive.")
            else:
                migrant.status = 'Active'
                print(f"Migrant {migrant.full_name} is now Active.")
            
            migrant.save()  # ✅ Save the status change after modification

            return JsonResponse({'success': True, 'new_status': migrant.status})
        
        except Migrant.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Migrant not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# ✅ View to display inactive workers
def inactive(request):
    contractor_id = request.session.get('contractor_id')

    if not contractor_id:
        return redirect('login')
    
    # ✅ Fetching all inactive workers for the logged-in contractor
    inactive_workers = Migrant.objects.filter(
        login__contractor__id=contractor_id,
        status='Inactive'
    )

    # ✅ Debugging to check how many inactive workers are found
    print(f"Inactive workers count: {inactive_workers.count()}")

    # ✅ Render inactive.html with the list of inactive workers
    return render(request, 'inactive.html', {'inactive_migrants': inactive_workers})


def payment_history(request):
    """Display payment history filtered by month and year."""
    contractor_id = request.session.get('contractor_id')

    # Get selected month and year
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    # Default to current month and year if not selected
    if not selected_month or not selected_year:
        selected_month = datetime.now().month
        selected_year = datetime.now().year

    # Fetch payments for selected month and year
    payments = SalaryPayment.objects.filter(
        contractor_id=contractor_id,
        month=selected_month,
        year=selected_year
    ).order_by('-paid_at')

    total_amount = payments.aggregate(Sum('salary_amount'))['salary_amount__sum'] or 0

    return render(request, 'payment_history.html', {
        'payments': payments,
        'month': int(selected_month),
        'year': int(selected_year),
        'total_amount': total_amount,
    })
    
    
from migrantapp.models import Contractor
from django.contrib import messages

def contractor_profile(request):
    contractor_id = request.session.get('contractor_id')
    contractor = Contractor.objects.get(id=contractor_id)
    return render(request, 'contractor_profile.html', {'contractor': contractor})
def edit_contractor_profile(request):
    contractor_id = request.session.get('contractor_id')
    contractor = Contractor.objects.get(id=contractor_id)

    if request.method == 'POST':
        contractor.name = request.POST['name']
        contractor.phone = request.POST['phone']
        contractor.location = request.POST['location']
        contractor.city = request.POST['city']
        contractor.district = request.POST['district']
        contractor.work_description = request.POST['work_description']

        if 'aadhaar_card' in request.FILES:
            contractor.aadhaar_card = request.FILES['aadhaar_card']

        contractor.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('contractor_profile')

    return render(request, 'edit_contractor_profile.html', {'contractor': contractor})