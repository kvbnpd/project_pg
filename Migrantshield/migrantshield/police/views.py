from django.shortcuts import render,redirect,get_object_or_404
from agentapp.models import NOC_application,NOC_table
from worker.models import Application_request
from django.http import JsonResponse
import pdfkit
import os
from django.utils.timezone import now
from migrantapp.models import Migrant
from .models import *
from django.conf import settings
from django.contrib import messages
# Create your views here.
def requests(request):
    return render(request,'requests.html')
def dashboard(request):
    return render(request,'dashboard.html')
def home(request):
    return render(request,'dashboard.html')
#def nocforapproval(request):
 #   applications = NOC_application.objects.filter(status='Applied')

def nocforapproval(request):
    station_id=request.session['police_id']
    #applications = NOC_application.objects.all()
    applications = NOC_application.objects.filter(
        migrant__application_request__contractor__police_station=station_id
    ).distinct()

    print(f"Total Applications Found: {applications.count()}", flush=True)

    for application in applications:
        application.migrant_details = application.migrant  # Fetch migrant details

        # Fetch the contractor details safely
        application_request = Application_request.objects.filter(migrant=application.migrant).first()
        
        if application_request:
            application.contractor_details = application_request.contractor

            print(f"\nApplication ID: {application.id}", flush=True)
            print(f"Migrant Name: {application.migrant_details.full_name}", flush=True)
            print(f"Migrant Aadhaar: {application.migrant_details.aadhaar}", flush=True)
            print(f"PCC File Path: {application.migrant_details.pcc.url}", flush=True)
            print(f"Photo Path: {application.migrant_details.photo.url}", flush=True)
            print(f"Contractor Name: {application.contractor_details.name}", flush=True)
        else:
            print(f"No Application_request found for migrant {application.migrant.full_name}", flush=True)

    return render(request, 'viewnocapplication.html', {'applications': applications})
def change_noc_to_processing(request,id):
    NOC_application.objects.filter(id=id).update(status="Processing")
    return redirect(nocforapproval)
 # Ensure models are correctly imported


def approve_noc(request):
    if request.method == "POST":
        try:
            appln_id = request.POST.get("appln_id")
            police_station = request.POST.get("police_station")
            district = request.POST.get("district")
            officer_name = request.POST.get("officer_name")
            designation = request.POST.get("designation")

            application = get_object_or_404(NOC_application, id=appln_id)
            migrant = application.migrant

            # ✅ Define correct path (without media/)
            pdf_dir = os.path.join(settings.MEDIA_ROOT, "NOC")
            os.makedirs(pdf_dir, exist_ok=True)  # Ensure directory exists

            # ✅ Generate HTML content
            pdf_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ text-align: center; font-size: 18px; font-weight: bold; }}
                    .content {{ margin-top: 20px; }}
                    .signature {{ margin-top: 50px; text-align: right; }}
                </style>
            </head>
            <body>
                <div class="header">
                    No Objection Certificate (NOC) <br>
                    (Issued by Kerala Police)
                </div>
                <p>
                    Police Department,<br>
                    {police_station},<br>
                    {district},<br>
                    Government of Kerala
                </p>
                <p>
                    Ref. No: NOC-{appln_id}<br>
                    Date: {now().strftime('%d/%m/%Y')}
                </p>
                <p>
                    To Whom It May Concern,
                </p>
                <p>
                    This is to certify that Mr./Ms. {migrant.full_name}, residing in {migrant.state}, 
                    has requested a No Objection Certificate (NOC) for official purposes.
                </p>
                <p>
                    As per our records, there are no adverse reports or criminal cases registered against the applicant 
                    at {police_station}. This certificate is issued upon the applicant’s request for the above-stated purpose.
                </p>
                <div class="signature">
                    Authorized Signatory,<br>
                    {officer_name}<br>
                    {designation}<br>
                    {police_station}
                </div>
            </body>
            </html>
            """

            # ✅ Specify wkhtmltopdf path
            pdfkit_config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

            # ✅ Save PDF file (Only "NOC/" as path)
            pdf_file_path = os.path.join(pdf_dir, f"NOC_{appln_id}.pdf")
            pdfkit.from_string(pdf_content, pdf_file_path, configuration=pdfkit_config)

            # ✅ Store only "NOC/NOC_34.pdf" (without media/)
            relative_path = os.path.join("NOC", f"NOC_{appln_id}.pdf")

            # ✅ Save details in database
            noc_entry = NOC_table.objects.create(
                Migrant=migrant,  # Ensure correct field name
                noc=relative_path  # Save only "NOC/NOC_34.pdf" (without media/)
            )

            application.status = "Approved"
            application.save()

            return JsonResponse({"status": "success", "noc_pdf": relative_path})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})
def add_crime_report(request):
    migrants = Migrant.objects.all()  # Fetch all migrants for dropdown
    if request.method == "POST":
        firnnumber=request.POST.get('firnumber')
        migrant_id = request.POST.get("migrant")
        crime_type = request.POST.get("crime_type")
        description = request.POST.get("description")
        status = request.POST.get("status")
        reported_by = request.POST.get("reported_by")
        reported_at = request.POST.get("reported_at")

        migrant = Migrant.objects.get(id=migrant_id)  # Get Migrant instance
        
        CrimeReport.objects.create(
            migrant=migrant,
            firnumber=firnnumber,
            crime_type=crime_type,
            description=description,
            status=status,
            reported_by=reported_by,
            reported_at=reported_at
        )
        
        messages.success(request, "Crime Report added successfully!")
        return redirect("add_crime_report")

    return render(request, "add_crime_report.html", {"migrants": migrants})

def view_all_cases(request):
    cases = CrimeReport.objects.all()  # Fetch all crime reports
    return render(request, 'view_all_cases.html', {'cases': cases})
def update_case(request, case_id):
    # Retrieve the specific case
    crime_case = get_object_or_404(CrimeReport, id=case_id)
    
    if request.method == "POST":
        # Get new status and resolving note from the form data
        new_status = request.POST.get("status")
        resolving_note = request.POST.get("resolving_note", "").strip()
        
        # Update the case attributes
        crime_case.status = new_status
        crime_case.resolving_note = resolving_note  # Ensure the field exists in your model
        
        # Save changes to the database
        crime_case.save()
        
        messages.success(request, "Case updated successfully!")
    
    # Redirect back to the view all cases page
    return redirect("view_all_cases")

def all_migrants(request):
    migrants = Migrant.objects.all()
    return render(request, 'all_migrants.html', {'migrants': migrants})

def migrantdet(request, migrant_id):
    migrant = get_object_or_404(Migrant, id=migrant_id)

    # Related data queries
    crime_reports = CrimeReport.objects.filter(migrant=migrant)
    application_requests = Application_request.objects.filter(migrant=migrant)
    noc_applications = NOC_application.objects.filter(migrant=migrant)
    noc_tables = NOC_table.objects.filter(Migrant=migrant)
    
    context = {
        'migrant': migrant,
        'crime_reports': crime_reports,
        'application_requests': application_requests,
        'noc_applications': noc_applications,
        'noc_tables': noc_tables,
      
    }
    print(f"DEBUG - Migrant: {migrant.full_name}")
    print("Crime Reports:", crime_reports.count())
    print("Application Requests:", application_requests.count())
    print("NOC Applications:", noc_applications.count())
    print("NOC Tables:", noc_tables.count())

    return render(request, 'migrantdet.html', context)