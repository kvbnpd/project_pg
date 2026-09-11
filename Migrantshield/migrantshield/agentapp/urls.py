from django.urls import path,include
from .import views

urlpatterns = [
    path('agenthome',views.agenthome,name='agenthome'),
      path('',views.agenthome,name='agenthome'),
      path('view_applications/', views.view_applications, name='view_applications'),
    path('update_application_status/<int:app_id>/<str:status>/', views.update_application_status, name='update_application_status'),
     path('view_new_applications/', views.view_new_applications, name='view_new_applications'),
     path('apply_noc_all/', views.apply_noc_all, name='apply_noc_all'),
     path("noc_status_page/", views.noc_status_page, name="noc_status_page"),  # NOC Status Page
    path("get_noc_status/", views.get_noc_status, name="get_noc_status"),  # API for fetching status
 path('download_noc/<int:migrant_id>', views.download_noc, name='download_noc'),
 path('myworkers', views.myworkers, name='myworkers'),
   path('download_idcard', views.download_idcard, name='download_idcard'),  
   path('download_id_card_individual/<int:migrant_id>', views.download_id_card_individual, name='download_id_card_individual'),  
   path('job_details_view', views.job_details_view, name='job_details_view'),
    path('delete-job/<int:job_id>/', views.delete_job_detail, name='delete_job'),
    path('schedule', views.schedule, name='schedule'),
    path('get-job-details/', views.get_job_details, name='get-job-details'),
    path('get-migrants/', views.get_migrants, name='get-migrants'),
    path('save-work-entry/', views.save_work_entry, name='save-work-entry'),
     path('view_schedule/<int:job_id>/', views.view_schedule, name='view_schedule'),
     path('select_month/', views.select_month, name='select_month'),
    path('pay_salary/', views.pay_salary, name='pay_salary'),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
     path('remove_migrant/', views.remove_migrant, name="remove_migrant"),
      path('job_requests/', views.job_requests, name='job_requests'),
      path("accept_job/<int:job_id>/", views.accept_job, name="accept_job"),
         path('mark_job_completed/<int:job_id>/', views.mark_job_completed, name='mark_job_completed'),
         path('myworkers/', views.myworkers, name='myworkers'),
   path('update_worker_status/', views.update_worker_status, name='update_migrant_status'),
    path('inactive/', views.inactive, name='inactive'),
     path('payment_history/', views.payment_history, name='payment_history'),
      path('contractor_profile/', views.contractor_profile, name='contractor_profile'),
    path('edit_contractor_profile/', views.edit_contractor_profile, name='edit_contractor_profile'),
     

]
  
