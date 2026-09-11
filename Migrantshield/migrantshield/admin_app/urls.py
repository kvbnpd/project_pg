from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      # Map to the admin_dashboard view
    path('worktype',views.worktype, name='worktype'),
    path('success',views.success, name='success'),
    path('adminhome',views.adminhome, name='adminhome'),
    #manage contractor
    path('view_pending_contractors', views.view_pending_contractors, name='view_pending_contractors'),
    path('approve_contractor/<int:contractor_id>/', views.approve_contractor, name='approve_contractor'),
    path('reject_contractor/<int:contractor_id>/', views.reject_contractor, name='reject_contractor'),
    path('view_active_contractors', views.view_active_contractors, name='view_active_contractors'),
    path('revoke_contractor/<int:contractor_id>/', views.revoke_contractor, name='revoke_contractor'),
    path('restore_contractor/<int:contractor_id>/', views.restore_contractor, name='restore_contractor'),
    #type of work
    path('view_type_of_work/', views.view_type_of_work, name='view_type_of_work'),
    path('delete_type_of_work/<int:work_id>/', views.delete_type_of_work, name='delete_type_of_work'),

    path('allmigrants', views.allmigrants, name='allmigrants'),
     path('migrant_detail/<int:migrant_id>', views.migrant_detail, name='migrant_detail'),
     path('view_payments/', views.view_payments, name='view_payments'),
     path("view_payment_details/<int:payment_id>/", views.view_payment_details, name="view_payment_details"),
     path('adminhome/', views.adminhome, name='adminhome'),
      path('api/dashboard-data/', views.get_dashboard_data, name='dashboard_data'),
     path('get_dashboard_data/', views.get_dashboard_data, name='get_dashboard_data'),
     path('crime-reports/', views.view_crime_reports, name='view_crime_reports'),
     path('views/', views.views, name='views'),
     path('user-queries/', views.view_user_queries, name='view_user_queries'),
     path('respond_query/<int:query_id>/', views.respond_query, name='respond_query'),
     path('add-police-station/', views.add_police_station, name='add_police_station'),
     path('edit_police_station/<int:id>/', views.edit_police_station, name='edit_police_station'),
    path('delete_police_station/<int:id>/', views.delete_police_station, name='delete_police_station'),
    
     

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
