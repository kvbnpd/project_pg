from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      path('requests',views.requests,name='requests'),
      path('dashboard',views.dashboard,name='dashboard'),
      path('home',views.home,name='home'),
      path('nocforapproval',views.nocforapproval,name='nocforapproval'),
      path('change_noc_to_processing/<int:id>',views.change_noc_to_processing,name='change_noc_to_processing'),
      path('approve_noc/', views.approve_noc, name='approve_noc'),
        path('add_crime_report/', views.add_crime_report, name='add_crime_report'),
         path('view_all_cases/', views.view_all_cases, name='view_all_cases'),
          path('update_case/<int:case_id>/', views.update_case, name='update_case'),
          path('all_migrants/', views.all_migrants, name='all_migrants'),
          path('migrantdet/<int:migrant_id>', views.migrantdet, name='migrantdet'),
]    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)