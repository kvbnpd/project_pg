from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
path('workerhome',views.workerhome,name='workerhome'),
path('apply_for_job/<int:contractor_id>/', views.apply_for_job, name='apply_for_job'),
path('check_application_status/', views.check_application_status, name='check_application_status'),
path('withdraw_application/<int:application_id>/', views.withdraw_application, name='withdraw_application'),
path('myhistory',views.myhistory,name='myhistory'),
path('mywork',views.mywork,name='mywork'),
path('myprofile',views.myprofile,name='myprofile'),
 path('edit_migrant_profile', views.edit_migrant_profile, name='edit_migrant_profile'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    

